import fastf1


def load_race(year, grand_prix):
    """
    Load race data for a specific Formula 1 Grand Prix.
    """

    fastf1.Cache.enable_cache("data/cache")

    session = fastf1.get_session(year, grand_prix, "R")
    session.load()

    return session
