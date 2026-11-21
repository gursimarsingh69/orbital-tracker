import httpx

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=JSON"

def fetch_satellite_data():
    print("Connecting to CelesTrak...")
    response = httpx.get(
        CELESTRAK_URL,
        timeout=30.0
    )
    response.raise_for_status()
    records = response.json()
    if not records:
        raise ValueError("No satellite data received")
    return records

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
