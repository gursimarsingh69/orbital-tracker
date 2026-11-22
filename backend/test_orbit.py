
from app.services.ingestion.celestrak import fetch_satellite_data
from app.services.orbital.propagation import calculate_position


records = fetch_satellite_data()

iss = records[0]

position = calculate_position(iss)

print("\nORBITWATCH - ISS POSITION")
print("=========================")

for key, value in position.items():
    print(f"{key}: {value}")
