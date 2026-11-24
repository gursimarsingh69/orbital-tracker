
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    source: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="running", nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    records_received: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    records_inserted: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    error_message: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    orbital_elements = relationship(
        "OrbitalElement",
        back_populates="ingestion_run"
    )
