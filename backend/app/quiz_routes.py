from datetime import datetime
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.module import Module
from app.models.learning_content import LearningContent, UserLearningContentProgress
from app.models.quiz import Quiz, Question, QuestionOption
from app.models.quiz_attempt import QuizAttempt, QuestionAttempt
from app.models.performance_analysis import PerformanceAnalysis
from app.auth.dependencies import get_current_user, require_admin, require_student
from app.quiz_schemas import (
    QuizCreate,
    QuizUpdate,
    QuizResponse,
    QuizStudentResponse,
    QuizSummaryResponse,
    QuizBankGenerateRequest,
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
    QuestionStudentResponse,
    QuestionOptionCreate,
    QuestionOptionUpdate,
    QuestionOptionResponse,
    QuestionOptionStudentResponse,
    QuizSubmissionRequest,
    QuizAttemptResultResponse,
    QuizAttemptSummaryResponse,
    QuestionAttemptResultResponse
)
from app.services.analytics_service import recalculate_student_module_progress, update_performance_analysis
from app.services.ai_assessment_service import generate_quiz_question_bank, generate_single_mcq_question

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


# ==========================================
# ACCESS & SELECTION HELPERS
# ==========================================

def _is_quiz_unlocked_for_student(db: Session, user: User, module_id: int) -> bool:
    """
    Checks if quiz is unlocked for student:
    - Admin always has access.
    - If module has 0 learning content items, unlocked.
    - If student completed all learning content items in module, unlocked.
    - If student previously passed the quiz, unlocked permanently.
    """
    if user.role == "admin":
        return True

    # Check if student previously passed any attempt for this module
    passed_attempt = db.query(QuizAttempt).join(
        Quiz, QuizAttempt.quiz_id == Quiz.id
    ).filter(
        Quiz.module_id == module_id,
        QuizAttempt.user_id == user.id,
        QuizAttempt.passed == True
    ).first()

    if passed_attempt:
        return True

    # Count total learning contents in module
    total_contents = db.query(LearningContent).filter(
        LearningContent.module_id == module_id
    ).count()

    if total_contents == 0:
        return True

    # Count completed contents by user
    completed_contents = db.query(UserLearningContentProgress).join(
        LearningContent,
        UserLearningContentProgress.learning_content_id == LearningContent.id
    ).filter(
        LearningContent.module_id == module_id,
        UserLearningContentProgress.user_id == user.id
    ).count()

    return completed_contents >= total_contents


def _select_attempt_questions(db: Session, quiz: Quiz, user_id: int) -> list[Question]:
    """
    Selects exactly 10 questions for a quiz attempt:
    - Target: 3 Easy, 4 Medium, 3 Hard.
    - Random selection preferring unseen questions.
    - Graceful fallback if fewer questions are available.
    - Returns up to 10 questions.
    """
    # 1. Approved questions in bank
    all_questions = db.query(Question).filter(
        Question.quiz_id == quiz.id,
        Question.is_approved == True
    ).all()

    if not all_questions:
        all_questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()

    if len(all_questions) <= 10:
        shuffled = list(all_questions)
        random.shuffle(shuffled)
        return shuffled

    # 2. Get previously seen question IDs for this user on this quiz
    seen_q_ids = set(
        qid for (qid,) in db.query(QuestionAttempt.question_id)
        .join(QuizAttempt, QuestionAttempt.attempt_id == QuizAttempt.id)
        .filter(QuizAttempt.quiz_id == quiz.id, QuizAttempt.user_id == user_id)
        .all()
    )

    # 3. Categorize by difficulty
    easy_q = [q for q in all_questions if (q.difficulty or "Medium").lower() == "easy"]
    med_q = [q for q in all_questions if (q.difficulty or "Medium").lower() == "medium"]
    hard_q = [q for q in all_questions if (q.difficulty or "Medium").lower() == "hard"]

    targets = [
        ("Easy", easy_q, 3),
        ("Medium", med_q, 4),
        ("Hard", hard_q, 3)
    ]

    selected = []
    selected_ids = set()

    for diff_name, pool, target_count in targets:
        unseen = [q for q in pool if q.id not in seen_q_ids]
        seen = [q for q in pool if q.id in seen_q_ids]
        random.shuffle(unseen)
        random.shuffle(seen)

        # Pick unseen first
        picked_unseen = unseen[:target_count]
        selected.extend(picked_unseen)
        selected_ids.update(q.id for q in picked_unseen)

        # If needed, fill from seen in same category
        needed = target_count - len(picked_unseen)
        if needed > 0:
            picked_seen = [q for q in seen if q.id not in selected_ids][:needed]
            selected.extend(picked_seen)
            selected_ids.update(q.id for q in picked_seen)

    # If still fewer than 10 questions (due to small difficulty pools)
    if len(selected) < 10:
        remaining_pool = [q for q in all_questions if q.id not in selected_ids]
        unseen_rem = [q for q in remaining_pool if q.id not in seen_q_ids]
        seen_rem = [q for q in remaining_pool if q.id in seen_q_ids]
        random.shuffle(unseen_rem)
        random.shuffle(seen_rem)

        needed = 10 - len(selected)
        picked_unseen = unseen_rem[:needed]
        selected.extend(picked_unseen)
        selected_ids.update(q.id for q in picked_unseen)

        needed = 10 - len(selected)
        if needed > 0:
            picked_seen = [q for q in seen_rem if q.id not in selected_ids][:needed]
            selected.extend(picked_seen)
            selected_ids.update(q.id for q in picked_seen)

    random.shuffle(selected)
    return selected[:10]


def _format_student_quiz_questions(questions: list[Question]) -> list[QuestionStudentResponse]:
    """
    Randomizes option order on every attempt and completely hides is_correct.
    """
    result = []
    for q in questions:
        shuffled_options = list(q.options)
        random.shuffle(shuffled_options)

        student_options = [
            QuestionOptionStudentResponse(
                id=opt.id,
                question_id=opt.question_id,
                option_text=opt.option_text,
                order_number=idx + 1
            )
            for idx, opt in enumerate(shuffled_options)
        ]

        result.append(
            QuestionStudentResponse(
                id=q.id,
                quiz_id=q.quiz_id,
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty=q.difficulty or "Medium",
                marks=q.marks or 4,
                order_number=len(result) + 1,
                options=student_options
            )
        )
    return result


# ==========================================
# ADMIN QUIZ CRUD
# ==========================================

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_in: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    module = db.query(Module).filter(Module.id == quiz_in.module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

    calculated_total_marks = quiz_in.total_marks
    if calculated_total_marks == 0:
        calculated_total_marks = sum(q.marks for q in quiz_in.questions) if quiz_in.questions else 40

    new_quiz = Quiz(
        module_id=quiz_in.module_id,
        title=quiz_in.title or f"{module.title} Quiz",
        description=quiz_in.description or f"Assessment quiz for {module.title}",
        total_marks=calculated_total_marks,
        pass_percentage=quiz_in.pass_percentage,
        time_limit_minutes=quiz_in.time_limit_minutes or 10
    )
    db.add(new_quiz)
    db.flush()

    for q_data in quiz_in.questions:
        question = Question(
            quiz_id=new_quiz.id,
            question_text=q_data.question_text,
            question_type=q_data.question_type,
            difficulty=q_data.difficulty or "Medium",
            marks=q_data.marks or 4,
            order_number=q_data.order_number,
            is_approved=q_data.is_approved
        )
        db.add(question)
        db.flush()

        for opt_data in q_data.options:
            option = QuestionOption(
                question_id=question.id,
                option_text=opt_data.option_text,
                is_correct=opt_data.is_correct,
                order_number=opt_data.order_number
            )
            db.add(option)

    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.get("/", response_model=list[QuizSummaryResponse])
def get_all_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quizzes = db.query(Quiz).all()
    result = []
    for q in quizzes:
        resp = QuizSummaryResponse.model_validate(q)
        resp.is_locked = not _is_quiz_unlocked_for_student(db, current_user, q.module_id)
        result.append(resp)
    return result


@router.get("/module/{module_id}", response_model=list[QuizSummaryResponse])
def get_quizzes_by_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    quizzes = db.query(Quiz).filter(Quiz.module_id == module_id).all()
    result = []
    for q in quizzes:
        resp = QuizSummaryResponse.model_validate(q)
        resp.is_locked = not _is_quiz_unlocked_for_student(db, current_user, module_id)
        result.append(resp)
    return result


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_admin(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz


@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,
    quiz_in: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    if quiz_in.title is not None:
        quiz.title = quiz_in.title
    if quiz_in.description is not None:
        quiz.description = quiz_in.description
    if quiz_in.total_marks is not None:
        quiz.total_marks = quiz_in.total_marks
    if quiz_in.pass_percentage is not None:
        quiz.pass_percentage = quiz_in.pass_percentage
    if quiz_in.time_limit_minutes is not None:
        quiz.time_limit_minutes = quiz_in.time_limit_minutes

    db.commit()
    db.refresh(quiz)
    return quiz


@router.delete("/{quiz_id}", status_code=status.HTTP_200_OK)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}


# ==========================================
# ADMIN QUESTION & OPTION CRUD
# ==========================================

@router.post("/{quiz_id}/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def add_question(
    quiz_id: int,
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    question = Question(
        quiz_id=quiz_id,
        question_text=question_in.question_text,
        question_type=question_in.question_type,
        difficulty=question_in.difficulty or "Medium",
        marks=question_in.marks or 4,
        order_number=question_in.order_number,
        is_approved=question_in.is_approved
    )
    db.add(question)
    db.flush()

    for opt_data in question_in.options:
        option = QuestionOption(
            question_id=question.id,
            option_text=opt_data.option_text,
            is_correct=opt_data.is_correct,
            order_number=opt_data.order_number
        )
        db.add(option)

    db.commit()
    db.refresh(question)
    return question


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    if question_in.question_text is not None:
        question.question_text = question_in.question_text
    if question_in.question_type is not None:
        question.question_type = question_in.question_type
    if question_in.difficulty is not None:
        question.difficulty = question_in.difficulty
    if question_in.marks is not None:
        question.marks = question_in.marks
    if question_in.order_number is not None:
        question.order_number = question_in.order_number
    if question_in.is_approved is not None:
        question.is_approved = question_in.is_approved

    db.commit()
    db.refresh(question)
    return question


@router.delete("/questions/{question_id}", status_code=status.HTTP_200_OK)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}


@router.post("/questions/{question_id}/options", response_model=QuestionOptionResponse, status_code=status.HTTP_201_CREATED)
def add_option(
    question_id: int,
    option_in: QuestionOptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    option = QuestionOption(
        question_id=question_id,
        option_text=option_in.option_text,
        is_correct=option_in.is_correct,
        order_number=option_in.order_number
    )
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


@router.put("/options/{option_id}", response_model=QuestionOptionResponse)
def update_option(
    option_id: int,
    option_in: QuestionOptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    option = db.query(QuestionOption).filter(QuestionOption.id == option_id).first()
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found"
        )

    if option_in.option_text is not None:
        option.option_text = option_in.option_text
    if option_in.is_correct is not None:
        option.is_correct = option_in.is_correct
    if option_in.order_number is not None:
        option.order_number = option_in.order_number

    db.commit()
    db.refresh(option)
    return option


@router.delete("/options/{option_id}", status_code=status.HTTP_200_OK)
def delete_option(
    option_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    option = db.query(QuestionOption).filter(QuestionOption.id == option_id).first()
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found"
        )
    db.delete(option)
    db.commit()
    return {"message": "Option deleted successfully"}


# ==========================================
# ADMIN AI QUESTION GENERATION & APPROVAL
# ==========================================

@router.post("/{quiz_id}/generate-bank", response_model=list[QuestionResponse], status_code=status.HTTP_201_CREATED)
def generate_ai_question_bank(
    quiz_id: int,
    req: QuizBankGenerateRequest = QuizBankGenerateRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    AI Question Bank Generator:
    Generates 30 MCQs (10 Easy, 10 Medium, 10 Hard) with 4 options each, marks=4, and 1 correct answer.
    Questions are stored in DB for Admin review/approval.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    module = db.query(Module).filter(Module.id == quiz.module_id).first()
    module_title = module.title if module else quiz.title
    module_desc = module.description if module else (quiz.description or "")

    generated_data = generate_quiz_question_bank(
        module_title=module_title,
        module_description=module_desc,
        count=req.count
    )

    created_questions = []
    current_count = db.query(Question).filter(Question.quiz_id == quiz.id).count()

    for idx, q_item in enumerate(generated_data, start=current_count + 1):
        q = Question(
            quiz_id=quiz.id,
            question_text=q_item["question_text"],
            question_type=q_item["question_type"],
            difficulty=q_item["difficulty"],
            marks=q_item["marks"],
            order_number=idx,
            is_approved=True  # Ready for admin review
        )
        db.add(q)
        db.flush()

        for opt_item in q_item["options"]:
            opt = QuestionOption(
                question_id=q.id,
                option_text=opt_item["option_text"],
                is_correct=opt_item["is_correct"],
                order_number=opt_item["order_number"]
            )
            db.add(opt)

        created_questions.append(q)

    db.commit()
    for q in created_questions:
        db.refresh(q)

    return created_questions


@router.post("/questions/{question_id}/approve", response_model=QuestionResponse)
def approve_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    question.is_approved = True
    db.commit()
    db.refresh(question)
    return question


@router.post("/{quiz_id}/approve-all")
def approve_all_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    db.query(Question).filter(Question.quiz_id == quiz.id).update({"is_approved": True})
    db.commit()
    return {"message": "All questions in quiz approved successfully"}


@router.post("/{quiz_id}/questions/{question_id}/replace", response_model=QuestionResponse)
def replace_rejected_question(
    quiz_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Replaces a rejected question with a newly generated AI question of the same difficulty.
    """
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.quiz_id == quiz_id
    ).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    module = db.query(Module).filter(Module.id == question.quiz.module_id).first()
    module_title = module.title if module else "Core Module Concept"

    new_q_data = generate_single_mcq_question(
        module_title=module_title,
        difficulty=question.difficulty or "Medium",
        order_number=question.order_number
    )

    # Delete existing options
    db.query(QuestionOption).filter(QuestionOption.question_id == question.id).delete()

    question.question_text = new_q_data["question_text"]
    question.difficulty = new_q_data["difficulty"]
    question.marks = new_q_data["marks"]
    question.is_approved = True
    db.flush()

    for opt in new_q_data["options"]:
        new_opt = QuestionOption(
            question_id=question.id,
            option_text=opt["option_text"],
            is_correct=opt["is_correct"],
            order_number=opt["order_number"]
        )
        db.add(new_opt)

    db.commit()
    db.refresh(question)
    return question


# ==========================================
# STUDENT QUIZ VIEW (is_correct HIDDEN)
# ==========================================

@router.get("/{quiz_id}/take", response_model=QuizStudentResponse)
def get_quiz_for_taking(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns 10 randomized questions with shuffled options for a student.
    Enforces module learning content completion lock.
    CRITICAL: is_correct is NOT included in the response.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    # Enforce quiz lock
    if not _is_quiz_unlocked_for_student(db, current_user, quiz.module_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz is locked. Please complete all learning content in this module first."
        )

    selected_questions = _select_attempt_questions(db, quiz, current_user.id)
    formatted_questions = _format_student_quiz_questions(selected_questions)

    total_marks = sum(q.marks for q in formatted_questions) if formatted_questions else 40

    return QuizStudentResponse(
        id=quiz.id,
        module_id=quiz.module_id,
        title=quiz.title,
        description=quiz.description,
        total_marks=total_marks,
        pass_percentage=quiz.pass_percentage,
        time_limit_minutes=quiz.time_limit_minutes or 10,
        total_questions=len(formatted_questions),
        questions=formatted_questions
    )


# ==========================================
# STUDENT QUIZ ATTEMPT & SUBMISSION
# ==========================================

@router.post("/{quiz_id}/start")
def start_quiz_attempt(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Starts a new quiz attempt:
    - Enforces lock status
    - Selects 10 randomized questions (3 Easy, 4 Med, 3 Hard, unseen preferred)
    - Shuffles options
    - Creates QuizAttempt record
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    # Check lock
    if not _is_quiz_unlocked_for_student(db, current_user, quiz.module_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz is locked. Please complete all learning content in this module first."
        )

    selected_questions = _select_attempt_questions(db, quiz, current_user.id)
    formatted_questions = _format_student_quiz_questions(selected_questions)
    total_marks = sum(q.marks for q in formatted_questions) if formatted_questions else 40

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=current_user.id,
        score=0.0,
        total_marks=float(total_marks),
        percentage=0.0,
        passed=False,
        started_at=datetime.now(),
        time_taken_seconds=0
    )
    db.add(attempt)
    db.flush()

    # Pre-register question attempts for the selected questions
    for q in selected_questions:
        qa = QuestionAttempt(
            attempt_id=attempt.id,
            question_id=q.id,
            selected_option_id=None,
            is_correct=False,
            marks_awarded=0.0
        )
        db.add(qa)

    db.commit()
    db.refresh(attempt)

    return {
        "message": "Quiz attempt started",
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "time_limit_minutes": quiz.time_limit_minutes or 10,
        "total_questions": len(formatted_questions),
        "total_marks": total_marks,
        "started_at": attempt.started_at,
        "questions": formatted_questions
    }


@router.post("/{quiz_id}/submit", response_model=QuizAttemptResultResponse)
def submit_quiz_attempt(
    quiz_id: int,
    submission: QuizSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits and grades a quiz attempt:
    - 4 marks per correct MCQ, 0 marks for incorrect or unanswered questions.
    - Max score = 40 (for 10 questions).
    - Passing score = >= 60% (24/40).
    - Evaluates 10-minute timer limit.
    - Updates student progress (permanently marks completed once passed) and module performance.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    # Locate or create attempt
    attempt = None
    if submission.attempt_id:
        attempt = db.query(QuizAttempt).filter(QuizAttempt.id == submission.attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz attempt not found"
            )
        if attempt.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to submit this attempt"
            )

    now = datetime.now()
    if not attempt:
        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=current_user.id,
            score=0.0,
            total_marks=40.0,
            percentage=0.0,
            passed=False,
            started_at=now,
            completed_at=now,
            time_taken_seconds=0
        )
        db.add(attempt)
        db.flush()

    # Time limit check (10 minutes = 600s + 60s grace period = 660s)
    elapsed_seconds = int((now - attempt.started_at).total_seconds()) if attempt.started_at else 0

    # Build question lookup
    quiz_questions = {q.id: q for q in quiz.questions}
    submitted_answers_map = {}

    for ans in submission.answers:
        if ans.question_id not in quiz_questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question ID {ans.question_id} does not belong to Quiz {quiz_id}"
            )
        question = quiz_questions[ans.question_id]
        valid_option_ids = {opt.id for opt in question.options}

        if ans.selected_option_id is not None and ans.selected_option_id not in valid_option_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Option ID {ans.selected_option_id} does not belong to Question {ans.question_id}"
            )
        submitted_answers_map[ans.question_id] = ans.selected_option_id

    # Determine which questions are evaluated
    # If attempt had pre-registered question attempts, use those questions; otherwise evaluate submitted questions (or all if short quiz)
    existing_qas = db.query(QuestionAttempt).filter(QuestionAttempt.attempt_id == attempt.id).all()
    if existing_qas:
        target_questions = [db.query(Question).filter(Question.id == qa.question_id).first() for qa in existing_qas]
        target_questions = [q for q in target_questions if q is not None]
    elif submitted_answers_map:
        target_questions = [quiz_questions[qid] for qid in submitted_answers_map if qid in quiz_questions]
    else:
        target_questions = list(quiz.questions[:10])

    if not target_questions:
        target_questions = list(quiz.questions[:10])

    # Grade questions
    total_score = 0.0
    total_quiz_marks = float(sum(q.marks or 4 for q in target_questions))
    if total_quiz_marks == 0.0:
        total_quiz_marks = 40.0

    # Delete previous question attempts for this attempt before rewriting
    db.query(QuestionAttempt).filter(QuestionAttempt.attempt_id == attempt.id).delete()

    question_results = []
    for question in target_questions:
        selected_option_id = submitted_answers_map.get(question.id)

        # Look up correct option in database
        correct_option = next((opt for opt in question.options if opt.is_correct), None)
        correct_option_id = correct_option.id if correct_option else None

        is_correct = (
            selected_option_id is not None and
            correct_option_id is not None and
            selected_option_id == correct_option_id
        )
        marks_awarded = float(question.marks or 4) if is_correct else 0.0
        total_score += marks_awarded

        q_attempt = QuestionAttempt(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected_option_id,
            is_correct=is_correct,
            marks_awarded=marks_awarded
        )
        db.add(q_attempt)

        question_results.append(
            QuestionAttemptResultResponse(
                question_id=question.id,
                question_text=question.question_text,
                selected_option_id=selected_option_id,
                correct_option_id=correct_option_id,
                is_correct=is_correct,
                marks_awarded=marks_awarded,
                max_marks=question.marks or 4
            )
        )

    percentage = round((total_score / total_quiz_marks * 100.0), 2) if total_quiz_marks > 0 else 0.0
    passed = percentage >= quiz.pass_percentage

    attempt.score = total_score
    attempt.total_marks = total_quiz_marks
    attempt.percentage = percentage
    attempt.passed = passed
    attempt.completed_at = now
    attempt.time_taken_seconds = min(elapsed_seconds, 600)

    db.commit()
    db.refresh(attempt)

    # Update progress and performance analysis
    recalculate_student_module_progress(
        db=db,
        user_id=current_user.id,
        module_id=quiz.module_id,
        latest_quiz_percentage=percentage,
        quiz_passed=passed
    )
    perf = update_performance_analysis(
        db=db,
        user_id=current_user.id,
        module_id=quiz.module_id
    )

    # Compute best score across all attempts for this quiz
    best_score = db.query(func.max(QuizAttempt.score)).filter(
        QuizAttempt.quiz_id == quiz.id,
        QuizAttempt.user_id == current_user.id
    ).scalar() or total_score

    return QuizAttemptResultResponse(
        attempt_id=attempt.id,
        quiz_id=attempt.quiz_id,
        user_id=attempt.user_id,
        score=attempt.score,
        total_marks=attempt.total_marks,
        percentage=attempt.percentage,
        passed=attempt.passed,
        latest_score=attempt.score,
        best_score=float(best_score),
        accuracy=perf.accuracy if perf else percentage,
        weakness_level=perf.weakness_level if perf else ("Strong" if percentage >= 80 else "Moderate" if percentage >= 60 else "Weak"),
        time_taken_seconds=attempt.time_taken_seconds,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
        question_results=question_results
    )


# ==========================================
# ATTEMPT HISTORY & RETAKE
# ==========================================

@router.get("/attempts/my", response_model=list[QuizAttemptSummaryResponse])
def get_my_quiz_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    View Attempt History: Returns previous attempts only when requested.
    """
    return db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed_at.isnot(None)
    ).order_by(QuizAttempt.completed_at.desc()).all()


@router.get("/{quiz_id}/attempts", response_model=list[QuizAttemptSummaryResponse])
def get_quiz_specific_attempts(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    View Attempt History for a specific quiz.
    """
    return db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed_at.isnot(None)
    ).order_by(QuizAttempt.completed_at.desc()).all()


@router.get("/attempts/{attempt_id}", response_model=QuizAttemptResultResponse)
def get_quiz_attempt_detail(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Detailed attempt view. Accessible only by owner or admin.
    """
    attempt = db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz attempt not found"
        )

    if current_user.role != "admin" and attempt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to access this attempt"
        )

    question_results = []
    for qa in attempt.question_attempts:
        question = db.query(Question).filter(Question.id == qa.question_id).first()
        correct_option = next((opt for opt in question.options if opt.is_correct), None) if question else None

        question_results.append(
            QuestionAttemptResultResponse(
                question_id=qa.question_id,
                question_text=question.question_text if question else "",
                selected_option_id=qa.selected_option_id,
                correct_option_id=correct_option.id if correct_option else None,
                is_correct=qa.is_correct,
                marks_awarded=qa.marks_awarded,
                max_marks=question.marks if question else 4
            )
        )

    quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
    perf = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.user_id == attempt.user_id,
        PerformanceAnalysis.module_id == (quiz.module_id if quiz else 1)
    ).first()

    best_score = db.query(func.max(QuizAttempt.score)).filter(
        QuizAttempt.quiz_id == attempt.quiz_id,
        QuizAttempt.user_id == attempt.user_id
    ).scalar() or attempt.score

    return QuizAttemptResultResponse(
        attempt_id=attempt.id,
        quiz_id=attempt.quiz_id,
        user_id=attempt.user_id,
        score=attempt.score,
        total_marks=attempt.total_marks,
        percentage=attempt.percentage,
        passed=attempt.passed,
        latest_score=attempt.score,
        best_score=float(best_score),
        accuracy=perf.accuracy if perf else attempt.percentage,
        weakness_level=perf.weakness_level if perf else "Moderate",
        time_taken_seconds=attempt.time_taken_seconds,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
        question_results=question_results
    )

