
from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id: Mapped[int] = mapped_column(primary_key=True)

    norad_catalog_id: Mapped[str] = mapped_column(
        String(16), unique=True, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    international_designator: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )

    object_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    orbital_elements = relationship(
        "OrbitalElement",
        back_populates="satellite",
        cascade="all, delete-orphan"
    )
