from five.yaml import load_yaml, to_sql
from five.tables import Films, FilmPicks, Series, SeriesPicks, Base
from five.tikz import graph_tikz_from_sql

import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

parser = argparse.ArgumentParser()
parser.add_argument("filename")

if __name__ == "__main__":
    args = parser.parse_args()

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yml = load_yaml(args.filename)
        to_sql(session, yml)

    graph_films = graph_tikz_from_sql(session, Films, FilmPicks)

    print(graph_films)

    graph_series = graph_tikz_from_sql(session, Series, SeriesPicks)
    print(graph_series)
