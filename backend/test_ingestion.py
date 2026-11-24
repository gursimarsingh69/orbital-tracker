from app.services.ingestion.celestrak import fetch_satellite_data
from app.services.ingestion.persist import ingest_records

try:
    records = fetch_satellite_data()
    result = ingest_records(records)

    print("\nORBITWATCH - INGESTION TEST")
    print("===========================")
    for key, value in result.items():
        print(f"{key}: {value}")

except Exception as error:
    print("Ingestion failed!")
    print(error)
