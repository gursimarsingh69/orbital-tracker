from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, desc

from app.database.session import SessionLocal
from app.models import Satellite, OrbitalElement
from app.services.orbital.propagation import calculate_position
from app.services.orbital.change_detection import (
    compare_orbital_records
)

router = APIRouter()


@router.get("/")
def get_satellites():

    with SessionLocal() as db:

        satellites = db.scalars(
            select(Satellite).order_by(Satellite.name)
        ).all()

        return [
            {
                "norad_id": satellite.norad_catalog_id,
                "name": satellite.name,
                "international_designator":
                    satellite.international_designator,
                "object_type": satellite.object_type
            }
            for satellite in satellites
        ]


@router.get("/{norad_id}/position")
def get_satellite_position(norad_id: str):

    with SessionLocal() as db:

        satellite = db.scalar(
            select(Satellite).where(
                Satellite.norad_catalog_id == norad_id
            )
        )

        if satellite is None:
            raise HTTPException(
                status_code=404,
                detail="Satellite not found"
            )

        orbital_element = db.scalar(
            select(OrbitalElement)
            .where(
                OrbitalElement.satellite_id == satellite.id
            )
            .order_by(desc(OrbitalElement.epoch))
            .limit(1)
        )

        if orbital_element is None:
            raise HTTPException(
                status_code=404,
                detail="No orbital elements available"
            )

        try:
            result = calculate_position(orbital_element.raw_omm)

            result["element_epoch"] = (
                orbital_element.epoch.isoformat()
            )

            return result

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Position calculation failed: {str(error)}"
            )


@router.get("/{norad_id}/history")
def get_orbital_history(
    norad_id: str,
    limit: int = Query(default=20, ge=1, le=100)
):
    with SessionLocal() as db:
        satellite = db.scalar(
            select(Satellite).where(
                Satellite.norad_catalog_id == norad_id
            )
        )

        if satellite is None:
            raise HTTPException(
                status_code=404,
                detail="Satellite not found"
            )

        records = db.scalars(
            select(OrbitalElement)
            .where(
                OrbitalElement.satellite_id == satellite.id
            )
            .order_by(OrbitalElement.epoch.desc())
            .limit(limit)
        ).all()

        formatted_records = [
            {
                "id": record.id,
                "epoch": record.epoch.isoformat(),
                "inclination": record.inclination,
                "eccentricity": record.eccentricity,
                "raan": record.raan,
                "argument_of_pericenter": record.argument_of_pericenter,
                "mean_anomaly": record.mean_anomaly,
                "mean_motion": record.mean_motion
            }
            for record in records
        ]

        return {
            "norad_id": norad_id,
            "satellite": satellite.name,
            "records_count": len(records),
            "records": formatted_records
        }

@router.get("/{norad_id}/changes")
def get_orbital_changes(
    norad_id: str,
    limit: int = Query(default=20, ge=2, le=100)
):

    with SessionLocal() as db:

        satellite = db.scalar(
            select(Satellite).where(
                Satellite.norad_catalog_id == norad_id
            )
        )

        if satellite is None:
            raise HTTPException(
                status_code=404,
                detail="Satellite not found"
            )

        records = db.scalars(
            select(OrbitalElement)
            .where(
                OrbitalElement.satellite_id == satellite.id
            )
            .order_by(OrbitalElement.epoch.desc())
            .limit(limit)
        ).all()

        # The comparison service expects chronological order.
        records = list(reversed(records))

        result = compare_orbital_records(records)

        return {
            "norad_id": norad_id,
            "satellite": satellite.name,
            "records_available": len(records),
            **result
        }

