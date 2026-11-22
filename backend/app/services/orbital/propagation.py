
from skyfield.api import load, wgs84, EarthSatellite


def calculate_position(omm_record: dict) -> dict:
    """
    Calculate the estimated geographic position of a satellite
    using its OMM orbital elements and SGP4 propagation.
    """

    ts = load.timescale()

    satellite = EarthSatellite.from_omm(ts, omm_record)

    t = ts.now()

    # Propagate satellite position to the selected time
    geocentric = satellite.at(t)

    # Geographic coordinates of the point below the satellite
    subpoint = wgs84.subpoint_of(geocentric)

    # Actual height of the satellite above the reference ellipsoid
    altitude = wgs84.height_of(geocentric)

    # Velocity vector in kilometres per second
    velocity = geocentric.velocity.km_per_s

    return {
        "satellite": omm_record.get("OBJECT_NAME"),
        "norad_id": str(omm_record.get("NORAD_CAT_ID")),
        "timestamp_utc": t.utc_iso(),
        "latitude": round(subpoint.latitude.degrees, 4),
        "longitude": round(subpoint.longitude.degrees, 4),
        "altitude_km": round(altitude.km, 2),
        "velocity_km_s": [
            round(float(v), 4) for v in velocity
        ]
    }
