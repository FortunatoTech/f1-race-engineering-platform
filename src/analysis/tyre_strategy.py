def get_tyre_strategies(session):
    """
    Reconstruct each driver's tyre strategy in stint order.
    """

    laps = session.laps.copy()

    laps = laps.dropna(subset=["Driver", "Compound", "Stint"])

    laps = laps.sort_values(["Driver", "Stint", "LapNumber"])

    stints = (
        laps.groupby(["Driver", "Stint"], sort=False)
        .agg(
            Compound=("Compound", "first"),
            StartLap=("LapNumber", "min"),
            EndLap=("LapNumber", "max"),
        )
        .reset_index()
    )

    stints["Stint"] = stints["Stint"].astype(int)
    stints["StartLap"] = stints["StartLap"].astype(int)
    stints["EndLap"] = stints["EndLap"].astype(int)

    return stints