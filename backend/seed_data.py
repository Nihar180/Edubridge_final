import os

from app.auth.security import hash_password
from app.database import SessionLocal
from app.models.grade import Grade
from app.models.learning_content import LearningContent
from app.models.module import Module
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.user import User

TOPICS = {
    "Mathematics": ("Algebra", "Geometry", "Fractions"),
    "Science": ("Physics", "Chemistry", "Biology"),
    "English": ("Grammar", "Vocabulary", "Reading"),
}

ALGEBRA_CONTENT = (
    "Algebra is a branch of mathematics that uses letters and symbols to represent unknown values.\n\n"
    "Examples:\n"
    "- x + 5 = 10, so x = 5.\n"
    "- 2x = 10, so x = 5.\n\n"
    "Key points:\n"
    "- Variables represent unknown values.\n"
    "- Expressions can contain numbers, variables, and operators.\n"
    "- Equations contain an equality sign."
)


def get_or_create(session, model, defaults=None, **filters):
    instance = session.query(model).filter_by(**filters).first()
    if instance:
        return instance

    instance = model(**filters, **(defaults or {}))
    session.add(instance)
    session.flush()
    return instance


def seed():
    password = os.getenv("SEED_USER_PASSWORD")
    if not password:
        raise RuntimeError("Set SEED_USER_PASSWORD before running the seed script.")

    username = os.getenv("SEED_USER_USERNAME", "teststudent")
    email = os.getenv("SEED_USER_EMAIL", "teststudent@edubridge.org")

    session = SessionLocal()
    try:
        grades = {}
        for grade_number in (8, 9, 10):
            grade = get_or_create(session, Grade, name=f"Grade {grade_number}")
            grades[grade_number] = grade

            for subject_name in ("Mathematics", "Science", "English"):
                subject = get_or_create(
                    session,
                    Subject,
                    grade_id=grade.id,
                    name=subject_name,
                    defaults={"description": f"{subject_name} for Grade {grade_number}"},
                )
                unit = get_or_create(
                    session,
                    Unit,
                    subject_id=subject.id,
                    title=f"Introduction to {subject_name}",
                    defaults={"description": "Core introductory unit", "order_number": 1},
                )
                existing_modules = session.query(Module).filter(
                    Module.unit_id == unit.id
                ).order_by(Module.order_number, Module.id).all()

                for index, topic_name in enumerate(TOPICS[subject_name], start=1):
                    topic_module = next(
                        (module for module in existing_modules if module.title == topic_name),
                        None,
                    )

                    if topic_module:
                        continue

                    placeholder = next(
                        (
                            module
                            for module in existing_modules
                            if module.title == f"{subject_name} Fundamentals"
                            and module.order_number == 1
                        ),
                        None,
                    )
                    if index == 1 and placeholder:
                        placeholder.title = topic_name
                        placeholder.description = f"{topic_name} learning module"
                        continue

                    topic_module = Module(
                        unit_id=unit.id,
                        title=topic_name,
                        description=f"{topic_name} learning module",
                        order_number=index,
                        difficulty="Medium",
                    )
                    session.add(topic_module)
                    session.flush()
                    existing_modules.append(topic_module)

        algebra_module = session.query(Module).join(Unit).join(Subject).filter(
            Subject.grade_id == grades[8].id,
            Subject.name == "Mathematics",
            Module.title == "Algebra",
        ).first()
        get_or_create(
            session,
            LearningContent,
            module_id=algebra_module.id,
            title="Algebra",
            defaults={
                "content_type": "text",
                "content": ALGEBRA_CONTENT,
                "media_url": None,
                "order_number": 1,
            },
        )

        user = session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if not user:
            user = User(
                name="Test Student",
                username=username,
                email=email,
                password_hash=hash_password(password),
                grade_id=grades[8].id,
                role="student",
            )
            session.add(user)

        session.commit()
        print(f"Seeded grades, hierarchy, and user '{username}'.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()