from pydantic import BaseModel


class GradeResponse(BaseModel):
    id: int
    name: str