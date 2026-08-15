from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, autoincrement=True)

    unit_id = Column(
        Integer,
        ForeignKey("units.id"),
        nullable=False
    )

    title = Column(
        String(150),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    order_number = Column(
        Integer,
        nullable=False
    )

    difficulty = Column(
        String(30),
        nullable=True
    )