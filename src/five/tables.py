from sqlalchemy.orm import DeclarativeBase, ForeignKey, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Films(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Games(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Picks(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))


class BookPicks(Picks):
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))


class FilmPicks(Picks):
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"))


class SeriesPicks(Picks):
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"))


class GamesPicks(Picks):
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
