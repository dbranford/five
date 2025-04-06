from five.yaml import load_yaml, to_sql
from five.tables import Films, Series, Books, Base

import argparse
from itertools import combinations
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from thefuzz import fuzz


def get_titles(session, table):
    titles = session.execute(select(table.name)).all()
    return [t[0] for t in titles]


parser = argparse.ArgumentParser()
parser.add_argument("filename")

if __name__ == "__main__":
    args = parser.parse_args()

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yml = load_yaml(args.filename)
        to_sql(session, yml)

        film_titles = get_titles(session, Films)
        series_titles = get_titles(session, Series)
        book_titles = get_titles(session, Books)

    print("Checking films")
    for t1, t2 in combinations(film_titles, 2):
        if 65 < fuzz.ratio(t1, t2) < 100:
            print(f"Possible overlap:\n- {t1}\n- {t2}")

    print("Checking series")
    for t1, t2 in combinations(series_titles, 2):
        if 65 < fuzz.ratio(t1, t2) < 100:
            print(f"Possible overlap:\n- {t1}\n- {t2}")

    print("Checking books")
    for t1, t2 in combinations(book_titles, 2):
        if 65 < fuzz.ratio(t1, t2) < 100:
            print(f"Possible overlap:\n- {t1}\n- {t2}")
