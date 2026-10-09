import re
import pandas as pd

def get_penalties(session):
    """
    Extract assigned penalties and match them with service messages.
    """


    messages = session.race_control_messages.copy()

    columns = [
        "Lap",
        "ServedLap",
        "Driver",
        "Type",
        "Seconds",
        "Reason",
        "Status",
        "Message",
    ]

    if messages.empty:
        return pd.DataFrame(columns=columns)

    penalties = []

    for _, row in messages.iterrows():
        message = str(row.get("Message", ""))

        # Ignore confirmation messages during the assignment pass.
        if re.search(r"\bPENALTY SERVED\b", message, re.IGNORECASE):
            continue

        # Identify penalty type and duration.
        if re.search(r"\bDRIVE THROUGH PENALTY\b", message, re.IGNORECASE):
            penalty_type = "DRIVE_THROUGH"
            seconds = None

        elif re.search(r"\bSTOP[\s-]*AND[\s-]*GO\b", message, re.IGNORECASE):
            penalty_type = "STOP_AND_GO"
            seconds = None

        else:
            match = re.search(
                r"\b(\d+)\s*SECOND(?:S)? TIME PENALTY\b",
                message,
                re.IGNORECASE,
            )

            if not match:
                continue

            penalty_type = "TIME_PENALTY"
            seconds = int(match.group(1))

        # Extract driver abbreviation.
        driver_match = re.search(
            r"\bCAR\s+\d+\s+\(([A-Z]{3})\)",
            message,
            re.IGNORECASE,
        )

        driver = driver_match.group(1).upper() if driver_match else None

        # Extract and clean the reason.
        reason_match = re.search(r"\s-\s(.+)", message)
        reason = reason_match.group(1).strip() if reason_match else None

        if reason:
            reason = re.sub(r"\s*\(\d{2}:\d{2}:\d{2}\)$", "", reason)

        penalties.append({
            "Lap": row.get("Lap"),
            "ServedLap": None,
            "Driver": driver,
            "Type": penalty_type,
            "Seconds": seconds,
            "Reason": reason,
            "Status": "ASSIGNED",
            "Message": message,
        })

    # Match each service message to the corresponding assigned penalty.
    for _, row in messages.iterrows():
        message = str(row.get("Message", ""))

        if not re.search(r"\bPENALTY SERVED\b", message, re.IGNORECASE):
            continue

        driver_match = re.search(
            r"\bCAR\s+\d+\s+\(([A-Z]{3})\)",
            message,
            re.IGNORECASE,
        )

        if not driver_match:
            continue

        driver = driver_match.group(1).upper()

        if re.search(r"\bDRIVE THROUGH PENALTY\b", message, re.IGNORECASE):
            penalty_type = "DRIVE_THROUGH"
            seconds = None

        else:
            match = re.search(
                r"\b(\d+)\s*SECOND(?:S)? TIME PENALTY\b",
                message,
                re.IGNORECASE,
            )

            if not match:
                continue

            penalty_type = "TIME_PENALTY"
            seconds = int(match.group(1))

        # Use the reason to avoid matching different penalties for the same driver.
        reason_match = re.search(
            r"\bPENALTY SERVED\b.*?\bPENALTY\b\s*-\s*(.+)",
            message,
            re.IGNORECASE,
        )

        served_reason = reason_match.group(1).strip() if reason_match else None

        if served_reason:
            served_reason = re.sub(
                r"\s*\(\d{2}:\d{2}:\d{2}\)$",
                "",
                served_reason,
            )

        candidates = [
            p for p in penalties
            if p["Driver"] == driver
            and p["Type"] == penalty_type
            and p["Seconds"] == seconds
            and p["Status"] == "ASSIGNED"
            and (
                served_reason is None
                or p["Reason"] == served_reason
            )
        ]

        if candidates:
            # If there are multiple matches, use the earliest still-unmatched one.
            penalty = min(
                candidates,
                key=lambda p: (
                    int(p["Lap"]) if pd.notna(p["Lap"]) else float("inf")
                ),
            )

            penalty["ServedLap"] = row.get("Lap")
            penalty["Status"] = "SERVED"
    
    for penalty in penalties:
        if penalty["Status"]== "ASSIGNED":
            penalty["Status"] = "ASSIGNED_UNCONFIRMED"
            
    return pd.DataFrame(penalties, columns=columns)

