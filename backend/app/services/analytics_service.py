from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_progress import StudentProgress
from app.models.performance_analysis import PerformanceAnalysis
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.question_attempt import QuestionAttempt
from app.models.learning_content import LearningContent, UserLearningContentProgress


def recalculate_student_module_progress(
    db: Session,
    user_id: int,
    module_id: int,
    latest_quiz_percentage: float | None = None,
    quiz_passed: bool | None = None
) -> StudentProgress:
    """
    Recalculates module progress according to rules:
    - Gradual progress from completing learning content items (e.g. 1/5 -> 20%, 5/5 -> 100%).
    - Module completion (100%) requires completing all learning content AND passing the quiz (>= 60%).
    - Once officially completed (100%), the module remains completed permanently.
    - mastery_score represents the student's BEST quiz performance for that module.
    """
    # 1. Total learning content in module
    total_contents = db.query(LearningContent).filter(
        LearningContent.module_id == module_id
    ).count()

    # 2. Completed learning contents by this user
    completed_contents = db.query(UserLearningContentProgress).join(
        LearningContent,
        UserLearningContentProgress.learning_content_id == LearningContent.id
    ).filter(
        LearningContent.module_id == module_id,
        UserLearningContentProgress.user_id == user_id
    ).count()

    content_percentage = (completed_contents / total_contents * 100.0) if total_contents > 0 else 100.0

    # 3. Check quiz state only when this module actually has quizzes.
    quiz_ids = [quiz_id for (quiz_id,) in db.query(Quiz.id).filter(
        Quiz.module_id == module_id
    ).all()]
    has_passed_quiz = False
    best_quiz_score = 0.0

    if quiz_ids:
        has_passed_quiz = db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id.in_(quiz_ids),
            QuizAttempt.user_id == user_id,
            QuizAttempt.passed == True
        ).first() is not None

        best_quiz_score = db.query(func.max(QuizAttempt.percentage)).filter(
            QuizAttempt.quiz_id.in_(quiz_ids),
            QuizAttempt.user_id == user_id
        ).scalar() or 0.0

    if quiz_passed:
        has_passed_quiz = True

    # 4. Fetch existing progress
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == user_id,
        StudentProgress.module_id == module_id
    ).first()

    # Determine completion percentage
    all_content_done = (completed_contents >= total_contents) if total_contents > 0 else True
    is_fully_completed = all_content_done and has_passed_quiz

    if is_fully_completed or (progress and progress.completion_percentage >= 100.0):
        final_completion_pct = 100.0
    else:
        final_completion_pct = round(content_percentage, 2)

    if latest_quiz_percentage is not None:
        best_quiz_score = max(float(best_quiz_score), float(latest_quiz_percentage))

    if progress:
        best_quiz_score = max(float(best_quiz_score), float(progress.mastery_score))

    final_mastery_score = round(float(best_quiz_score), 2)

    if not progress:
        progress = StudentProgress(
            user_id=user_id,
            module_id=module_id,
            completion_percentage=final_completion_pct,
            mastery_score=final_mastery_score,
            last_accessed=datetime.now()
        )
        db.add(progress)
    else:
        progress.last_accessed = datetime.now()
        # Permanence rule: Never decrease completion if already 100%
        if progress.completion_percentage < 100.0:
            progress.completion_percentage = max(progress.completion_percentage, final_completion_pct)
        # Mastery rule: Never decrease mastery score
        progress.mastery_score = max(progress.mastery_score, final_mastery_score)

    db.commit()
    db.refresh(progress)
    return progress


def update_student_progress(
    db: Session,
    user_id: int,
    module_id: int,
    completion_percentage: float | None = None,
    mastery_score: float | None = None
) -> StudentProgress:
    """
    Direct progress update with fallback to recalculate.
    """
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == user_id,
        StudentProgress.module_id == module_id
    ).first()

    if not progress:
        progress = StudentProgress(
            user_id=user_id,
            module_id=module_id,
            completion_percentage=completion_percentage if completion_percentage is not None else 0.0,
            mastery_score=mastery_score if mastery_score is not None else 0.0,
            last_accessed=datetime.now()
        )
        db.add(progress)
    else:
        progress.last_accessed = datetime.now()
        if completion_percentage is not None:
            if progress.completion_percentage < 100.0 or completion_percentage >= 100.0:
                progress.completion_percentage = max(progress.completion_percentage, completion_percentage)
        if mastery_score is not None:
            progress.mastery_score = max(progress.mastery_score, mastery_score)

    db.commit()
    db.refresh(progress)
    return progress


def update_performance_analysis(
    db: Session,
    user_id: int,
    module_id: int | None = None
) -> PerformanceAnalysis:
    """
    Calculates module-wise performance analysis.
    Weakness levels:
    - 80-100% -> Strong
    - 60-79% -> Moderate
    - Below 60% -> Weak
    """
    # If module_id is None, find all modules the user has attempts in
    if module_id is None:
        first_quiz_attempt = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.completed_at.isnot(None)
        ).order_by(QuizAttempt.completed_at.desc()).first()

        if first_quiz_attempt:
            quiz = db.query(Quiz).filter(Quiz.id == first_quiz_attempt.quiz_id).first()
            if quiz:
                module_id = quiz.module_id

    if module_id is None:
        # Fallback to module 1 if no attempts exist yet
        module_id = 1

    # Fetch attempts for this user for quizzes in this module
    attempts = db.query(QuizAttempt).join(
        Quiz, QuizAttempt.quiz_id == Quiz.id
    ).filter(
        Quiz.module_id == module_id,
        QuizAttempt.user_id == user_id,
        QuizAttempt.completed_at.isnot(None)
    ).all()

    total_attempts = len(attempts)
    attempt_ids = [a.id for a in attempts]

    if attempt_ids:
        q_attempts = db.query(QuestionAttempt).filter(
            QuestionAttempt.attempt_id.in_(attempt_ids)
        ).all()
        total_questions = len(q_attempts)
        correct_answers = sum(1 for qa in q_attempts if qa.is_correct)
    else:
        total_questions = 0
        correct_answers = 0

    accuracy = round((correct_answers / total_questions * 100.0), 2) if total_questions > 0 else 0.0

    if accuracy >= 80.0:
        weakness_level = "Strong"
    elif accuracy >= 60.0:
        weakness_level = "Moderate"
    else:
        weakness_level = "Weak"

    performance = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.user_id == user_id,
        PerformanceAnalysis.module_id == module_id
    ).first()

    if not performance:
        performance = PerformanceAnalysis(
            user_id=user_id,
            module_id=module_id,
            total_attempts=total_attempts,
            correct_answers=correct_answers,
            total_questions=total_questions,
            accuracy=accuracy,
            weakness_level=weakness_level,
            updated_at=datetime.now()
        )
        db.add(performance)
    else:
        performance.total_attempts = total_attempts
        performance.correct_answers = correct_answers
        performance.total_questions = total_questions
        performance.accuracy = accuracy
        performance.weakness_level = weakness_level
        performance.updated_at = datetime.now()

    db.commit()
    db.refresh(performance)
    return performance

