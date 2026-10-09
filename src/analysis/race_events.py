import pandas as pd

def get_race_events(session):
    """
    Extract and classify relevant race-control messages.
    """

    messages = session.race_control_messages.copy()

    if messages.empty:
        return pd.DataFrame(
            columns=["Time", "Lap", "Category", "Message"]
        )

    messages["Message"] = messages["Message"].fillna("")

    rules = {
         "PIT_LANE_TRANSIT": r"ALL CARS THROUGH THE PIT LANE",
         "RED_FLAG": r"RED FLAG\s*-\s*RACE SUSPENDED",
         "SAFETY_CAR": r"SAFETY CAR|VIRTUAL SAFETY CAR|\bVSC\b",
         "DRIVE_THROUGH": r"DRIVE THROUGH",
         "STOP_AND_GO": r"STOP[\s-]*AND[\s-]*GO",
         "TIME_PENALTY": r"\b\d+\s*SECOND(?:S)? TIME PENALTY",
         "INVESTIGATION": r"UNDER INVESTIGATION|WILL BE INVESTIGATED",
         "NO_FURTHER_ACTION": r"NO FURTHER ACTION", 
    }
    events = []

    for _, row in messages.iterrows():
        message = row["Message"]
        
        for category, pattern in rules.items():
            if pd.Series([message]).str.contains(
                pattern, case=False, regex=True
            ).iloc[0]:
               events.append({
                "Time": row.get("Time"),
                "Lap": row.get("Lap"),
                "Category": category,
                "Message": message,
               })
               break
    return pd.DataFrame(
        events, 
        columns=["Time", "Lap", "Category","Message"]
    )
