import pandas as pd

def get_race_pace(session):

    """
    Extract clean lap times for each driver from a race session.
    """

    laps = session.laps.copy()

    laps = laps[
        laps["LapTime"].notna()
        & laps["PitInTime"].isna()
        & laps["PitOutTime"].isna()
        & laps["IsAccurate"].eq(True)
    ].copy()

    laps["LapTimeSeconds"]= laps["LapTime"].dt.total_seconds()
    laps["LapNumber"] = laps["LapNumber"].astype(int)

    return laps[
        ["Driver", "LapNumber", "LapTimeSeconds", "Compound"]
    ]

def filter_completed_drivers(laps, race_results):
    """
    Keep only drivers who completed at least 75% of the race.
    """

    race_laps = int(race_results["Laps"].max())
    minimum_laps = race_laps * 0.75

    completed_drivers = race_results[
        race_results["Laps"] >= minimum_laps
    ]["Abbreviation"]

    return laps[laps["Driver"].isin(completed_drivers)].copy()

def filter_race_pace(laps):
    """
    Remove unusually slow laps for each driver using the IQR method.
    """

    def remove_outliers(group):
        q1 = group["LapTimeSeconds"].quantile(0.25)
        q3 = group["LapTimeSeconds"].quantile(0.75)
        iqr = q3 - q1

        upper_limit = q3 + 1.5 * iqr

        return group[group["LapTimeSeconds"] <= upper_limit]

    return (
        laps
        .groupby("Driver", group_keys=False)
        .apply(remove_outliers)
        .reset_index(drop=True)
    )
