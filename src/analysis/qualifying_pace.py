import pandas as pd


def get_qualifying_speeds(session, drivers=None):
    """
    Calculate the maximum telemetry speed for each valid qualifying lap.

    Parameters
    ----------
    session : FastF1 Session
        A loaded qualifying session.
    drivers : list[str] or None
        Optional list of driver abbreviations for testing.

    Returns
    -------
    pandas.DataFrame
        One row per valid lap, with lap time and maximum speed.
    """

    columns = [
        "Driver",
        "LapNumber",
        "LapTimeSeconds",
        "SpeedMaxKmh",
    ]

    laps = session.laps.copy()

    # Keep valid laps and exclude pit-entry and pit-exit laps.
    valid_laps = laps[
        laps["LapTime"].notna()
        & laps["IsAccurate"].eq(True)
        & laps["PitInTime"].isna()
        & laps["PitOutTime"].isna()
    ].copy()

    if "Deleted" in laps.columns:
        valid_laps = valid_laps[
            ~valid_laps["Deleted"].fillna(False)
        ].copy()

    # Optionally restrict the analysis to selected drivers.
    if drivers is not None:
        valid_laps = valid_laps[
            valid_laps["Driver"].isin(drivers)
        ]
    
     # Convert lap times to seconds.
    valid_laps["LapTimeSeconds"] = (
        valid_laps["LapTime"].dt.total_seconds()
    )

    # Exclude laps more than 5% slower than each driver's
    # best remaining lap.
    best_times = valid_laps.groupby("Driver")[
        "LapTimeSeconds"
    ].transform("min")

    valid_laps = valid_laps[
        valid_laps["LapTimeSeconds"] <= best_times * 1.05
    ].copy()

    records = []

    for _, lap in valid_laps.iterrows():
        driver = lap["Driver"]
        lap_number = int(lap["LapNumber"])


        # Retrieve telemetry for this specific driver's lap.
        one_lap = (
            session.laps
            .pick_drivers(driver)
            .pick_laps(lap_number)
        )

        if one_lap.empty:
            continue

        telemetry = one_lap.get_telemetry()

        if telemetry.empty or "Speed" not in telemetry.columns:
            continue

        max_speed = telemetry["Speed"].max()

        if pd.isna(max_speed):
            continue

        records.append({
            "Driver": driver,
            "LapNumber": lap_number,
            "LapTimeSeconds": lap["LapTimeSeconds"],
            "SpeedMaxKmh": float(max_speed),
        })

    return pd.DataFrame(records, columns=columns)
