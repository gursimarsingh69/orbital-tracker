import httpx
import time

CELESTRAK_URL = (
    "https://celestrak.org/NORAD/elements/"
    "gp.php?CATNR=25544&FORMAT=JSON"
)

CACHE_TTL = 2 * 60 * 60  # 2 hours

_cached_records = None
_last_fetch_time = 0.0


def fetch_satellite_data(force_refresh=False):

    global _cached_records, _last_fetch_time

    current_time = time.monotonic()

    # Check whether valid cached data exists
    if (
        not force_refresh
        and _cached_records is not None
        and current_time - _last_fetch_time < CACHE_TTL
    ):
        print("Using cached CelesTrak data...")
        return _cached_records

    print("Fetching satellite data from CelesTrak...")

    response = httpx.get(
        CELESTRAK_URL,
        timeout=30.0
    )

    response.raise_for_status()

    records = response.json()

    if not records:
        raise ValueError("No satellite data received")

    # Save data in memory
    _cached_records = records
    _last_fetch_time = time.monotonic()

    print("Satellite data cached successfully.")

    return _cached_records

def main():
    records = fetch_satellite_data()
    for satellite in records:
        print("\nSatellite Information")
        print("---------------------")
        print("Name:", satellite.get("OBJECT_NAME"))
        print("NORAD ID:", satellite.get("NORAD_CAT_ID"))
        print("Epoch:", satellite.get("EPOCH"))
        print("Inclination:", satellite.get("INCLINATION"))
        print("Eccentricity:", satellite.get("ECCENTRICITY"))
        print("Mean Motion:", satellite.get("MEAN_MOTION"))

if __name__ == "__main__":
    main()
