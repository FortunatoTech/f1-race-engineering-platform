from src.data.fastf1_client import load_session
from src.analysis.race_pace import (
    get_race_pace,
    filter_completed_drivers,
    filter_race_pace,
)
from src.analysis.qualifying_pace import get_qualifying_speeds
from src.visualization.race_pace_plot import plot_race_pace
from src.visualization.qualifying_speed_plot import (
    plot_qualifying_speeds,
)


def main():
    print("=== F1 Race Engineering Platform ===")
    print("1. Race pace — passo gara")
    print("2. Qualifying speed — velocità in qualifica")

    choice = input("Scegli un'analisi (1 o 2): ").strip()
    year_text = input("Anno del campionato (es. 2026): ").strip()
    grand_prix = input("Gran Premio (es. Monaco): ").strip()

    try:
        year = int(year_text)
    except ValueError:
        print("Errore: inserisci un anno valido.")
        return

    if choice == "1":
        session = load_session(year, grand_prix, "R")

        laps = get_race_pace(session)
        laps = filter_completed_drivers(laps, session.results)
        laps = filter_race_pace(laps)

        if laps.empty:
            print("Nessun dato di passo gara disponibile.")
            return

        plot_race_pace(laps, grand_prix, year)

    elif choice == "2":
        session = load_session(year, grand_prix, "Q")
        speeds = get_qualifying_speeds(session)

        if speeds.empty:
            print("Nessun dato di velocità in qualifica disponibile.")
            return

        plot_qualifying_speeds(speeds, grand_prix, year)

    else:
        print("Scelta non valida. Riavvia il programma e scegli 1 o 2.")


if __name__ == "__main__":
    main()
