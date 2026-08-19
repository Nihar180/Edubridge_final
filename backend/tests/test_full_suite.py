import os
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, SessionLocal
from app.models.user import User
from app.models.grade import Grade
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.module import Module
from app.models.learning_content import LearningContent, UserLearningContentProgress
from app.models.quiz import Quiz, Question, QuestionOption
from app.models.quiz_attempt import QuizAttempt, QuestionAttempt
from app.models.student_progress import StudentProgress
from app.models.performance_analysis import PerformanceAnalysis
from app.auth.security import hash_password, create_access_token

client = TestClient(app)


def test_01_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "EduBridge API is running"}


def test_02_auth_and_roles_setup():
    db = SessionLocal()
    try:
        # Ensure a grade exists
        grade = db.query(Grade).first()
        if not grade:
            grade = Grade(name="Grade 10")
            db.add(grade)
            db.commit()
            db.refresh(grade)
        grade_id = grade.id

        # Ensure admin user
        admin = db.query(User).filter(User.username == "admin_test").first()
        if not admin:
            admin = User(
                name="Admin Tester",
                username="admin_test",
                email="admin_test@edubridge.test",
                password_hash=hash_password("adminpass123"),
                role="admin",
                grade_id=grade_id
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # Ensure student user 1
        student1 = db.query(User).filter(User.username == "student_test1").first()
        if not student1:
            student1 = User(
                name="Student One",
                username="student_test1",
                email="student1@edubridge.test",
                password_hash=hash_password("studentpass123"),
                role="student",
                grade_id=grade_id
            )
            db.add(student1)
            db.commit()
            db.refresh(student1)

        # Ensure student user 2
        student2 = db.query(User).filter(User.username == "student_test2").first()
        if not student2:
            student2 = User(
                name="Student Two",
                username="student_test2",
                email="student2@edubridge.test",
                password_hash=hash_password("studentpass123"),
                role="student",
                grade_id=grade_id
            )
            db.add(student2)
            db.commit()
            db.refresh(student2)

        # Ensure subject, unit, module
        subject = db.query(Subject).first()
        if not subject:
            subject = Subject(grade_id=grade_id, name="Mathematics", description="Core Math")
            db.add(subject)
            db.commit()
            db.refresh(subject)

        unit = db.query(Unit).first()
        if not unit:
            unit = Unit(subject_id=subject.id, title="Algebra Foundations", description="Polynomials and equations", order_number=1)
            db.add(unit)
            db.commit()
            db.refresh(unit)

        module = db.query(Module).first()
        if not module:
            module = Module(unit_id=unit.id, title="Linear Equations", description="Solving 1-variable equations", order_number=1, difficulty="Easy")
            db.add(module)
            db.commit()
            db.refresh(module)

    finally:
        db.close()


def test_03_login_and_tokens():
    # Admin login
    resp_admin = client.post("/auth/login", json={"username": "admin_test", "password": "adminpass123"})
    assert resp_admin.status_code == 200
    assert "access_token" in resp_admin.json()

    # Student login
    resp_student = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    assert resp_student.status_code == 200
    assert "access_token" in resp_student.json()

    # Test invalid login
    resp_invalid = client.post("/auth/login", json={"username": "admin_test", "password": "wrongpassword"})
    assert resp_invalid.status_code == 401


def test_04_user_profile_endpoints():
    login_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # GET /profiles/me
    get_resp = client.get("/profiles/me", headers=headers)
    assert get_resp.status_code == 200
    profile_data = get_resp.json()
    assert profile_data["username"] == "student_test1"

    # PUT /profiles/me
    put_resp = client.put(
        "/profiles/me",
        headers=headers,
        json={
            "preferred_language": "Spanish",
            "learning_goal": "Master high-school algebra",
            "profile_image_url": "https://example.com/avatar.png"
        }
    )
    assert put_resp.status_code == 200
    updated = put_resp.json()
    assert updated["preferred_language"] == "Spanish"
    assert updated["learning_goal"] == "Master high-school algebra"
    assert updated["profile_image_url"] == "https://example.com/avatar.png"


def test_05_learning_content_gradual_progress_and_quiz_unlock():
    admin_resp = client.post("/auth/login", json={"username": "admin_test", "password": "adminpass123"})
    admin_headers = {"Authorization": f"Bearer {admin_resp.json()['access_token']}"}

    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    db = SessionLocal()
    unit = db.query(Unit).first()
    # Create fresh module for testing 5-content gradual progress
    test_mod = Module(unit_id=unit.id, title="Gradual Progress Module", description="5 content items", order_number=99)
    db.add(test_mod)
    db.commit()
    db.refresh(test_mod)
    module_id = test_mod.id
    db.close()

    # Upload a test file
    dummy_file_content = b"%PDF-1.4 dummy pdf content for testing"
    upload_resp = client.post(
        "/learning-contents/upload",
        headers=admin_headers,
        files={"file": ("lecture_notes.pdf", dummy_file_content, "application/pdf")}
    )
    assert upload_resp.status_code == 200
    media_url = upload_resp.json()["media_url"]

    # Create 5 learning contents in this module
    content_ids = []
    for i in range(1, 6):
        lc_resp = client.post(
            "/learning-contents/",
            headers=admin_headers,
            json={
                "module_id": module_id,
                "title": f"Lesson Item {i}",
                "content_type": "pdf" if i == 1 else "text",
                "content": f"Educational material {i}",
                "media_url": media_url if i == 1 else None,
                "order_number": i
            }
        )
        assert lc_resp.status_code == 201
        content_ids.append(lc_resp.json()["id"])

    # Create a quiz for this module to test locking
    quiz_resp = client.post(
        "/quizzes/",
        headers=admin_headers,
        json={"module_id": module_id, "title": "Gradual Quiz", "total_marks": 40, "pass_percentage": 60.0}
    )
    assert quiz_resp.status_code == 201
    quiz_id = quiz_resp.json()["id"]

    # Step 0: Quiz MUST be locked initially before any learning content is completed
    locked_attempt = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers)
    assert locked_attempt.status_code == 403, "Quiz must be locked before completing learning contents!"

    # Complete items 1 to 5 step by step and verify gradual progress (20%, 40%, 60%, 80%, 100%)
    expected_pcts = [20.0, 40.0, 60.0, 80.0, 100.0]
    for idx, c_id in enumerate(content_ids):
        comp_resp = client.post(f"/learning-contents/{c_id}/complete", headers=student_headers)
        assert comp_resp.status_code == 200
        comp_data = comp_resp.json()
        assert comp_data["module_content_completion_percentage"] == expected_pcts[idx]
        if idx < 4:
            assert comp_data["all_content_completed"] is False
            assert comp_data["quiz_unlocked"] is False
            # Quiz still locked
            assert client.post(f"/quizzes/{quiz_id}/start", headers=student_headers).status_code == 403
        else:
            assert comp_data["all_content_completed"] is True
            assert comp_data["quiz_unlocked"] is True
            # Quiz is now unlocked!
            unlocked_resp = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers)
            assert unlocked_resp.status_code == 200


def test_06_admin_quiz_creation_and_ai_question_bank():
    admin_resp = client.post("/auth/login", json={"username": "admin_test", "password": "adminpass123"})
    admin_headers = {"Authorization": f"Bearer {admin_resp.json()['access_token']}"}

    db = SessionLocal()
    module = db.query(Module).first()
    module_id = module.id
    db.close()

    # Admin creates Quiz with time limit of 10 minutes
    quiz_payload = {
        "module_id": module_id,
        "title": "Linear Equations Comprehensive Quiz",
        "description": "30 Question Bank Assessment",
        "total_marks": 40,
        "pass_percentage": 60.0,
        "time_limit_minutes": 10
    }
    create_resp = client.post("/quizzes/", headers=admin_headers, json=quiz_payload)
    assert create_resp.status_code == 201
    quiz_id = create_resp.json()["id"]
    assert create_resp.json()["time_limit_minutes"] == 10

    # Admin triggers AI Question Bank Generation (30 MCQs: 10 Easy, 10 Med, 10 Hard, 4 options each, marks=4)
    gen_resp = client.post(f"/quizzes/{quiz_id}/generate-bank", headers=admin_headers, json={"count": 30})
    assert gen_resp.status_code == 201
    questions = gen_resp.json()
    assert len(questions) == 30

    # Verify each question has exactly 4 options, difficulty, 4 marks, and is_approved
    easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
    med_count = sum(1 for q in questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
    assert easy_count == 10
    assert med_count == 10
    assert hard_count == 10

    for q in questions:
        assert len(q["options"]) == 4
        assert q["marks"] == 4
        assert q["is_approved"] is True
        correct_opts = [o for o in q["options"] if o["is_correct"]]
        assert len(correct_opts) == 1

    # Admin tests replacing a rejected question
    first_q_id = questions[0]["id"]
    replace_resp = client.post(f"/quizzes/{quiz_id}/questions/{first_q_id}/replace", headers=admin_headers)
    assert replace_resp.status_code == 200
    rep_data = replace_resp.json()
    assert rep_data["id"] == first_q_id
    assert len(rep_data["options"]) == 4


def test_07_student_quiz_start_and_randomization():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    db = SessionLocal()
    quiz = db.query(Quiz).order_by(Quiz.id.desc()).first()
    quiz_id = quiz.id
    db.close()

    # Student starts attempt
    start_resp = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers)
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    attempt_id = start_data["attempt_id"]
    questions = start_data["questions"]

    # Student receives exactly 10 questions
    assert len(questions) == 10
    assert start_data["total_marks"] == 40
    assert start_data["time_limit_minutes"] == 10

    # Verify difficulty distribution: 3 Easy, 4 Medium, 3 Hard
    easy_q = [q for q in questions if q["difficulty"] == "Easy"]
    med_q = [q for q in questions if q["difficulty"] == "Medium"]
    hard_q = [q for q in questions if q["difficulty"] == "Hard"]
    assert len(easy_q) == 3
    assert len(med_q) == 4
    assert len(hard_q) == 3

    # CRITICAL CHECK: is_correct is NOT exposed anywhere to student
    for q in questions:
        assert len(q["options"]) == 4
        for opt in q["options"]:
            assert "is_correct" not in opt


def test_08_quiz_submission_scoring_and_pass_criteria():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    admin_resp = client.post("/auth/login", json={"username": "admin_test", "password": "adminpass123"})
    admin_headers = {"Authorization": f"Bearer {admin_resp.json()['access_token']}"}

    db = SessionLocal()
    quiz = db.query(Quiz).order_by(Quiz.id.desc()).first()
    quiz_id = quiz.id
    db.close()

    # Start fresh attempt
    start_resp = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers)
    start_data = start_resp.json()
    attempt_id = start_data["attempt_id"]
    attempt_questions = start_data["questions"]

    # Fetch correct options using admin endpoint
    admin_quiz = client.get(f"/quizzes/{quiz_id}", headers=admin_headers).json()
    correct_map = {}
    for q in admin_quiz["questions"]:
        correct_opt = next(o["id"] for o in q["options"] if o["is_correct"])
        correct_map[q["id"]] = correct_opt

    # Submit 8 correct answers and 2 unanswered/incorrect -> 8 * 4 = 32 marks (80%, Pass)
    submission_answers = []
    for idx, q in enumerate(attempt_questions):
        if idx < 8:
            submission_answers.append({"question_id": q["id"], "selected_option_id": correct_map[q["id"]]})
        else:
            submission_answers.append({"question_id": q["id"], "selected_option_id": None})

    sub_resp = client.post(
        f"/quizzes/{quiz_id}/submit",
        headers=student_headers,
        json={"attempt_id": attempt_id, "answers": submission_answers}
    )
    assert sub_resp.status_code == 200
    res = sub_resp.json()

    assert res["score"] == 32.0
    assert res["total_marks"] == 40.0
    assert res["percentage"] == 80.0
    assert res["passed"] is True
    assert res["latest_score"] == 32.0
    assert res["best_score"] >= 32.0
    assert res["weakness_level"] in ["Strong", "Moderate", "Weak"]
    assert len(res["question_results"]) == 10


def test_09_unlimited_retakes_mastery_and_completion_permanence():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    db = SessionLocal()
    quiz = db.query(Quiz).order_by(Quiz.id.desc()).first()
    quiz_id = quiz.id
    module_id = quiz.module_id
    db.close()

    # Retake 1: Score 36/40 (90%)
    start1 = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers).json()
    attempt1_id = start1["attempt_id"]

    # Submit with attempt1
    admin_resp = client.post("/auth/login", json={"username": "admin_test", "password": "adminpass123"})
    admin_quiz = client.get(f"/quizzes/{quiz_id}", headers={"Authorization": f"Bearer {admin_resp.json()['access_token']}"}).json()
    correct_map = {q["id"]: next(o["id"] for o in q["options"] if o["is_correct"]) for q in admin_quiz["questions"]}

    sub1_answers = [{"question_id": q["id"], "selected_option_id": correct_map[q["id"]]} for q in start1["questions"][:9]]
    res1 = client.post(f"/quizzes/{quiz_id}/submit", headers=student_headers, json={"attempt_id": attempt1_id, "answers": sub1_answers}).json()
    assert res1["score"] == 36.0
    assert res1["best_score"] == 36.0

    # Retake 2: Intentionally fail with 16/40 (40%)
    start2 = client.post(f"/quizzes/{quiz_id}/start", headers=student_headers).json()
    attempt2_id = start2["attempt_id"]
    sub2_answers = [{"question_id": q["id"], "selected_option_id": correct_map[q["id"]]} for q in start2["questions"][:4]]
    res2 = client.post(f"/quizzes/{quiz_id}/submit", headers=student_headers, json={"attempt_id": attempt2_id, "answers": sub2_answers}).json()
    assert res2["score"] == 16.0
    assert res2["passed"] is False

    # Check mastery score in progress (must remain 90% and completion must remain 100%)
    prog_resp = client.get(f"/progress/module/{module_id}", headers=student_headers)
    assert prog_resp.status_code == 200
    prog = prog_resp.json()
    assert prog["completion_percentage"] == 100.0, "Module completion must remain permanent!"
    assert prog["mastery_score"] >= 90.0, "Mastery score must track best attempt!"


def test_10_attempt_history_and_isolation():
    student1_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student1_headers = {"Authorization": f"Bearer {student1_resp.json()['access_token']}"}

    student2_resp = client.post("/auth/login", json={"username": "student_test2", "password": "studentpass123"})
    student2_headers = {"Authorization": f"Bearer {student2_resp.json()['access_token']}"}

    # Student 1 gets my attempts
    history_resp = client.get("/quizzes/attempts/my", headers=student1_headers)
    assert history_resp.status_code == 200
    attempts = history_resp.json()
    assert len(attempts) >= 2
    attempt_id = attempts[0]["id"]

    # Student 1 can view own attempt detail
    own_detail = client.get(f"/quizzes/attempts/{attempt_id}", headers=student1_headers)
    assert own_detail.status_code == 200

    # Student 2 CANNOT view student 1's attempt (Security check)
    other_detail = client.get(f"/quizzes/attempts/{attempt_id}", headers=student2_headers)
    assert other_detail.status_code == 403


def test_11_module_performance_analysis():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    db = SessionLocal()
    module = db.query(Module).first()
    module_id = module.id
    db.close()

    # GET /performance/me
    perf_resp = client.get("/performance/me", headers=student_headers)
    assert perf_resp.status_code == 200
    perf = perf_resp.json()
    assert perf["total_attempts"] >= 2
    assert perf["weakness_level"] in ["Strong", "Moderate", "Weak"]

    # GET /performance/module/{module_id}
    mod_perf_resp = client.get(f"/performance/module/{module_id}", headers=student_headers)
    assert mod_perf_resp.status_code == 200
    mod_perf = mod_perf_resp.json()
    assert mod_perf["module_id"] == module_id
    assert mod_perf["total_attempts"] >= 2


def test_12_unit_assessment_practice_reference():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    db = SessionLocal()
    unit = db.query(Unit).first()
    unit_id = unit.id
    db.close()

    ua_resp = client.get(f"/unit-assessments/unit/{unit_id}", headers=student_headers)
    assert ua_resp.status_code == 200
    data = ua_resp.json()

    assert data["total_short_answer_questions"] == 10
    assert data["total_long_answer_questions"] == 10
    assert len(data["short_answer_questions"]) == 10
    assert len(data["long_answer_questions"]) == 10

    for q in data["short_answer_questions"]:
        assert q["question_type"] == "short_answer"
        assert "is_correct" not in q

    for q in data["long_answer_questions"]:
        assert q["question_type"] == "long_answer"
        assert "is_correct" not in q


def test_13_role_authorization_and_edge_cases():
    student_resp = client.post("/auth/login", json={"username": "student_test1", "password": "studentpass123"})
    student_headers = {"Authorization": f"Bearer {student_resp.json()['access_token']}"}

    # Student cannot create quiz
    quiz_create = client.post("/quizzes/", headers=student_headers, json={"module_id": 1, "title": "Hacked Quiz"})
    assert quiz_create.status_code == 403

    # Student cannot generate question bank
    gen_bank = client.post("/quizzes/1/generate-bank", headers=student_headers)
    assert gen_bank.status_code == 403

    # Student cannot approve questions
    approve_q = client.post("/quizzes/questions/1/approve", headers=student_headers)
    assert approve_q.status_code == 403

    # Invalid quiz submission question ID
    bad_sub = client.post("/quizzes/1/submit", headers=student_headers, json={"answers": [{"question_id": 999999, "selected_option_id": 1}]})
    assert bad_sub.status_code == 400

    # Unauthenticated request
    unauth = client.get("/profiles/me")
    assert unauth.status_code in [401, 403]
