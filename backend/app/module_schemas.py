from pydantic import BaseModel


class ModuleCreate(BaseModel):
    unit_id: int
    title: str
    description: str | None = None
    order_number: int
    difficulty: str | None = None


class ModuleResponse(BaseModel):
    id: int
    unit_id: int
    title: str
    description: str | None = None
    order_number: int
    difficulty: str | None = None