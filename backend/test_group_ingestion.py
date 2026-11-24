
from app.services.ingestion.celestrak import fetch_group_data
from app.services.ingestion.persist import ingest_records


print("\nORBITWATCH MULTI-SATELLITE INGESTION")
print("====================================")

# Fetch multiple satellite records
records = fetch_group_data("STATIONS")

print(f"\nRecords received: {len(records)}")

# Display a preview
print("\nSATELLITE PREVIEW")
print("-----------------")

for record in records[:10]:
    print(
        record.get("OBJECT_NAME"),
        "| NORAD:",
        record.get("NORAD_CAT_ID")
    )

# Save records into PostgreSQL
print("\nSTARTING DATABASE INGESTION")

result = ingest_records(records)

print("\nINGESTION SUMMARY")
print("-----------------")

for key, value in result.items():
    print(f"{key}: {value}")
