
from app.services.ingestion.celestrak import fetch_group_data
from app.services.ingestion.persist import ingest_records


def collect_orbital_history(group="STATIONS"):

    print("\nORBITWATCH HISTORICAL DATA COLLECTION")
    print("=====================================")

    records = fetch_group_data(
        group=group,
        force_refresh=True
    )

    print(f"Records fetched: {len(records)}")

    result = ingest_records(records)

    print("\nCOLLECTION SUMMARY")
    print("------------------")

    for key, value in result.items():
        print(f"{key}: {value}")

    return result


if __name__ == "__main__":
    collect_orbital_history()
