
from datetime import datetime

from sqlalchemy import (
    String, Float, DateTime, ForeignKey, JSON, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OrbitalElement(Base):
    __tablename__ = "orbital_elements"

    __table_args__ = (
        UniqueConstraint(
            "satellite_id",
            "epoch",
            "checksum",
            name="uq_satellite_epoch_checksum"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    satellite_id: Mapped[int] = mapped_column(
        ForeignKey("satellites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ingestion_run_id: Mapped[int] = mapped_column(
        ForeignKey("ingestion_runs.id"),
        nullable=False
    )

    epoch: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    inclination: Mapped[float] = mapped_column(Float, nullable=False)
    eccentricity: Mapped[float] = mapped_column(Float, nullable=False)
    raan: Mapped[float] = mapped_column(Float, nullable=False)
    argument_of_pericenter: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    mean_anomaly: Mapped[float] = mapped_column(Float, nullable=False)
    mean_motion: Mapped[float] = mapped_column(Float, nullable=False)

    checksum: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    raw_omm: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )

    satellite = relationship(
        "Satellite",
        back_populates="orbital_elements"
    )

    ingestion_run = relationship(
        "IngestionRun",
        back_populates="orbital_elements"
    )
