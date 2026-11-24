
import hashlib
import json

from datetime import datetime, timezone

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import Satellite, OrbitalElement, IngestionRun


def calculate_checksum(record: dict) -> str:
    """Generate a stable SHA-256 checksum for an OMM record."""

    serialized = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def parse_epoch(epoch_string: str) -> datetime:
    """Convert OMM epoch into a timezone-aware datetime."""

    return datetime.fromisoformat(
        epoch_string.replace("Z", "+00:00")
    )


def ingest_records(records: list[dict]) -> dict:

    with SessionLocal() as db:

        run = IngestionRun(
            source="CelesTrak",
            status="running",
            records_received=len(records)
        )

        db.add(run)
        db.flush()

        inserted = 0
        duplicates = 0

        try:

            for record in records:

                norad_id = str(record["NORAD_CAT_ID"])

                # Find existing satellite
                satellite = db.scalar(
                    select(Satellite).where(
                        Satellite.norad_catalog_id == norad_id
                    )
                )

                # Create satellite if it doesn't exist
                if satellite is None:

                    satellite = Satellite(
                        norad_catalog_id=norad_id,
                        name=record["OBJECT_NAME"],
                        international_designator=record.get("OBJECT_ID")
                    )

                    db.add(satellite)
                    db.flush()

                epoch = parse_epoch(record["EPOCH"])
                checksum = calculate_checksum(record)

                # Prevent duplicate orbital records
                existing = db.scalar(
                    select(OrbitalElement.id).where(
                        OrbitalElement.satellite_id == satellite.id,
                        OrbitalElement.epoch == epoch,
                        OrbitalElement.checksum == checksum
                    )
                )

                if existing is not None:
                    duplicates += 1
                    continue

                orbital_element = OrbitalElement(
                    satellite_id=satellite.id,
                    ingestion_run_id=run.id,
                    epoch=epoch,
                    inclination=float(record["INCLINATION"]),
                    eccentricity=float(record["ECCENTRICITY"]),
                    raan=float(record["RA_OF_ASC_NODE"]),
                    argument_of_pericenter=float(
                        record["ARG_OF_PERICENTER"]
                    ),
                    mean_anomaly=float(record["MEAN_ANOMALY"]),
                    mean_motion=float(record["MEAN_MOTION"]),
                    checksum=checksum,
                    raw_omm=record
                )

                db.add(orbital_element)
                inserted += 1

            run.records_inserted = inserted
            run.status = "completed"
            run.completed_at = datetime.now(timezone.utc)

            db.commit()

            return {
                "status": "success",
                "records_received": len(records),
                "records_inserted": inserted,
                "duplicates_skipped": duplicates
            }

        except Exception as error:
            db.rollback()
            raise error
