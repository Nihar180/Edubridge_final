from pydantic import BaseModel


class UnitCreate(BaseModel):
    subject_id: int
    title: str
    description: str | None = None
    order_number: int


class UnitResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    description: str | None = None
    order_number: int