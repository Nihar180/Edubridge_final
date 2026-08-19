import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_full_suite import (
    test_01_root_endpoint,
    test_02_auth_and_roles_setup,
    test_03_login_and_tokens,
    test_04_user_profile_endpoints,
    test_05_learning_content_gradual_progress_and_quiz_unlock,
    test_06_admin_quiz_creation_and_ai_question_bank,
    test_07_student_quiz_start_and_randomization,
    test_08_quiz_submission_scoring_and_pass_criteria,
    test_09_unlimited_retakes_mastery_and_completion_permanence,
    test_10_attempt_history_and_isolation,
    test_11_module_performance_analysis,
    test_12_unit_assessment_practice_reference,
    test_13_role_authorization_and_edge_cases
)

tests = [
    ("01 - Root Endpoint", test_01_root_endpoint),
    ("02 - Auth & Roles Setup", test_02_auth_and_roles_setup),
    ("03 - Login & JWT Tokens", test_03_login_and_tokens),
    ("04 - User Profile Endpoints", test_04_user_profile_endpoints),
    ("05 - Learning Content Gradual Progress & Quiz Unlock", test_05_learning_content_gradual_progress_and_quiz_unlock),
    ("06 - Admin Quiz Creation, 10-min Timer & AI 30-Question Bank", test_06_admin_quiz_creation_and_ai_question_bank),
    ("07 - Student Quiz Start (10 MCQs: 3 Easy/4 Med/3 Hard, Shuffled Options, Hidden Answers)", test_07_student_quiz_start_and_randomization),
    ("08 - Quiz Submission, 40-Mark Scoring & >=60% Pass Threshold", test_08_quiz_submission_scoring_and_pass_criteria),
    ("09 - Unlimited Retakes, Best Score Mastery & Module Completion Permanence", test_09_unlimited_retakes_mastery_and_completion_permanence),
    ("10 - Attempt History Endpoint & Student Security Isolation", test_10_attempt_history_and_isolation),
    ("11 - Module-Wise Performance Analysis (Strong / Moderate / Weak)", test_11_module_performance_analysis),
    ("12 - Unit Assessment 20 Practice Questions (10 SAQ + 10 LAQ, Reference Only)", test_12_unit_assessment_practice_reference),
    ("13 - Role Authorization & Security Edge Cases", test_13_role_authorization_and_edge_cases)
]

print("=" * 60)
print("RUNNING EDUBRIDGE BACKEND VERIFICATION TEST SUITE")
print("=" * 60)

passed = 0
failed = 0

for name, test_fn in tests:
    try:
        test_fn()
        print(f"  [PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        import traceback
        traceback.print_exc()
        failed += 1

print("=" * 60)
print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests.")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
