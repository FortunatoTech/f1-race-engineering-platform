import matplotlib.pyplot as plt


def plot_race_pace(laps, grand_prix, year):
    """
    Plot race pace distributions, ordered by median lap time.
    The gap under each driver is relative to the fastest median.
    """

    # Calculate the median lap time for each driver.
    medians = laps.groupby("Driver")["LapTimeSeconds"].median()
    medians = medians.sort_values()

    # Fastest driver becomes the reference.
    reference_driver = medians.index[0]
    reference_time = medians.iloc[0]

    # Sort the boxplots from fastest to slowest.
    drivers = medians.index.tolist()
    lap_times = [
        laps.loc[laps["Driver"] == driver, "LapTimeSeconds"].values
        for driver in drivers
    ]

    # Calculate the gap relative to the reference.
    gaps = medians - reference_time

    labels = [
        f"{driver}\n{gap:+.3f} s"
        if driver != reference_driver
        else f"{driver}\nREF."
        for driver, gap in gaps.items()
    ]

    fig, ax = plt.subplots(figsize=(16, 8))

    ax.boxplot(
        lap_times,
        tick_labels=labels,
        showfliers=False,
        patch_artist=True,
    )

    ax.set_title(
        f"Race Pace — {grand_prix} {year}\n"
        f"Reference: {reference_driver} "
        f"({reference_time:.3f} s median)"
    )
    ax.set_xlabel("Driver and median pace gap")
    ax.set_ylabel("Lap time (seconds)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.setp(ax.get_xticklabels(), fontsize=9)

    fig.tight_layout()
    plt.show()
