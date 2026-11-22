
from app.services.ingestion.celestrak import fetch_satellite_data

print("\nFIRST REQUEST")
first = fetch_satellite_data()

print("\nSECOND REQUEST")
second = fetch_satellite_data()

print("\nTHIRD REQUEST")
third = fetch_satellite_data()

print("\nCACHE TEST")
print("First and second identical:", first is second)
print("Second and third identical:", second is third)
