import matplotlib.pyplot as plt

def plot_qualifying_speeds(speeds, grand_prix, year):
    """
    Plot the distribution of maximum telemetry speeds per valid lap.

    Drivers are ordered by median maximum speed, from highest to lowest.
    """

    #Calculate the median speed for each driver.
    medians = (
        speeds.groupby("Driver")["SpeedMaxKmh"]
        .median()
        .sort_values(ascending=False)
    )

    drivers = medians.index.tolist()

    #Prepare the speed distribution for each driver.
    distributions = [
        speeds.loc[
            speeds["Driver"] == driver, "SpeedMaxKmh"
        ].dropna().values
        for driver in drivers
    ]

    fig, ax = plt.subplots(figsize=(16,8))

    violin = ax.violinplot(
        distributions,
        showmedians=True,
        showextrema=True,
    )

    ax.set_xticks(range(1,len(drivers)+1))
    ax.set_xticklabels(drivers)

    ax.set_title(
        f"Qualifying Maximum Speed - {grand_prix} {year}\n"
        "Per-lap maximum telemetry speed, valid laps only"
    )
    ax.set_xlabel("Driver (ordered by median speed)")
    ax.set_ylabel("Maximum speed per lap (km/h)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax.text(
        0.99,
        0.02,
        "Violin = distribution | Line = median",
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=9,
    )

    plt.setp(ax.get_xticklabels(), fontsize=9)

    fig.tight_layout()
    plt.show()