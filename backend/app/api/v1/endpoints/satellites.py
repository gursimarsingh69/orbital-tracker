from fastapi import APIRouter, HTTPException
from app.services.ingestion.celestrak import fetch_satellite_data
from app.services.orbital.propagation import calculate_position

router = APIRouter()


@router.get("/{norad_id}/position")
def get_satellite_position(norad_id: str):
    try:
        records = fetch_satellite_data()

        satellite = next(
            (
                record for record in records
                if str(record.get("NORAD_CAT_ID")) == norad_id
            ),
            None
        )

        if satellite is None:
            raise HTTPException(
                status_code=404,
                detail="Satellite not found"
            )

        return calculate_position(satellite)

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Satellite data processing failed: {str(error)}"
        )
