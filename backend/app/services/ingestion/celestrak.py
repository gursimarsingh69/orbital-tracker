
import httpx
import time

# Separate cache for satellite groups
_group_cache = {}

GROUP_CACHE_TTL = 2 * 60 * 60


def fetch_group_data(group="STATIONS", force_refresh=False):
    """
    Fetch OMM JSON records for a CelesTrak satellite group.
    """

    current_time = time.monotonic()

    cached = _group_cache.get(group)

    # Return cached records if they are still fresh
    if (
        not force_refresh
        and cached is not None
        and current_time - cached["fetched_at"] < GROUP_CACHE_TTL
    ):
        print(f"Using cached {group} data...")
        return cached["records"]

    url = (
        "https://celestrak.org/NORAD/elements/"
        f"gp.php?GROUP={group}&FORMAT=JSON"
    )

    print(f"Fetching CelesTrak group: {group}")

    response = httpx.get(url, timeout=60.0)
    response.raise_for_status()

    records = response.json()

    if not isinstance(records, list) or not records:
        raise ValueError(f"No valid records received for {group}")

    # Cache the complete group
    _group_cache[group] = {
        "records": records,
        "fetched_at": time.monotonic()
    }

    print(f"Successfully retrieved {len(records)} records.")

    return records


def fetch_satellite_data(norad_id="25544", force_refresh=False):
    """
    Fetch single satellite or group data for backward compatibility.
    """
    records = fetch_group_data("STATIONS", force_refresh=force_refresh)
    matching = [
        r for r in records
        if str(r.get("NORAD_CAT_ID")) == str(norad_id)
    ]
    if matching:
        return matching
    return records
