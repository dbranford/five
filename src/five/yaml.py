import yaml
from .tables import (
    People,
    Books,
    Films,
    Series,
    Games,
    BookPicks,
    FilmPicks,
    SeriesPicks,
    GamesPicks,
)
from sqlalchemy.orm import Session


def load_yaml(file) -> dict:
    with open(file) as f:
        data = yaml.safe_load(f)
        return data


def to_sql(session: Session, data: dict):
    for year, year_picks in data.items():
        for pick_type, people in year_picks.items():
            match pick_type:
                case "books":
                    curr_type = Books
                    curr_pick = BookPicks
                case "films":
                    curr_type = Films
                    curr_pick = FilmPicks
                case "series":
                    curr_type = Series
                    curr_pick = SeriesPicks
                case "games":
                    curr_type = Games
                    curr_pick = GamesPicks
                case _:
                    raise ValueError("Unrecognised type")
            for person, picks in people.items():
                person_id = People.find_or_insert(session, person)
                pick_ids = {curr_type.find_or_insert(session, pick) for pick in picks}
                picks_entries = {
                    curr_pick(year=year, pick_id=pick_id, person_id=person_id)
                    for pick_id in pick_ids
                }
                session.add_all(picks_entries)
                session.commit()
