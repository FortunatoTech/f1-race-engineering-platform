import fastf1


def load_session(year, grand_prix, session_type):
    """
    Load a Formula 1 session.

    Parameters
    ----------
    year : int
        Championship year.
    grand_prix : str
        Grand Prix name, for example "Monaco".
    session_type : str
        Session identifier, for example "R" for Race
        or "Q" for Qualifying.
    """

    fastf1.Cache.enable_cache("data/cache")

    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()

    return session


def load_race(year, grand_prix):
    """
    Load a race session.
    """

    return load_session(year, grand_prix, "R")

