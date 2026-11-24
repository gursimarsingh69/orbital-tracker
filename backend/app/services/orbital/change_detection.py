
def angular_difference(current: float, previous: float) -> float:
    """
    Calculate the shortest signed angular difference.
    Handles transitions such as 359 degrees -> 1 degree.
    """
    return (current - previous + 180) % 360 - 180


def compare_orbital_records(records: list) -> dict:
    """
    Compare consecutive orbital element records.

    Records must be ordered chronologically.
    """

    if len(records) < 2:
        return {
            "status": "insufficient_data",
            "message": "At least two distinct orbital epochs are required.",
            "comparisons": []
        }

    comparisons = []

    for previous, current in zip(records, records[1:]):

        elapsed_hours = (
            current.epoch - previous.epoch
        ).total_seconds() / 3600

        if elapsed_hours <= 0:
            continue

        changes = {
            "inclination_deg": round(
                current.inclination - previous.inclination, 8
            ),
            "eccentricity": round(
                current.eccentricity - previous.eccentricity, 10
            ),
            "raan_deg": round(
                angular_difference(current.raan, previous.raan), 8
            ),
            "argument_of_pericenter_deg": round(
                angular_difference(
                    current.argument_of_pericenter,
                    previous.argument_of_pericenter
                ), 8
            ),
            "mean_anomaly_deg": round(
                angular_difference(
                    current.mean_anomaly,
                    previous.mean_anomaly
                ), 8
            ),
            "mean_motion_rev_per_day": round(
                current.mean_motion - previous.mean_motion, 10
            )
        }

        comparisons.append({
            "previous_epoch": previous.epoch.isoformat(),
            "current_epoch": current.epoch.isoformat(),
            "elapsed_hours": round(elapsed_hours, 4),
            "changes": changes
        })

    return {
        "status": "success",
        "records_compared": len(comparisons),
        "comparisons": comparisons
    }
