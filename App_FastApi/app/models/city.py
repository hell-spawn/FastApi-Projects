from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    country: Mapped[str] = mapped_column(index=True)
    population: Mapped[int] = mapped_column(nullable=True)
