from pydantic import BaseModel


class SubjectCreate(BaseModel):
    grade_id: int
    name: str
    description: str | None = None


class SubjectResponse(BaseModel):
    id: int
    grade_id: int
    name: str
    description: str | None = None