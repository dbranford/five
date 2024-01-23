from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, synonym
from sqlalchemy import ForeignKey, select


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    @classmethod
    def find_or_insert(cls, session: Session, thing) -> int:
        stmt = select(cls).where(cls.name == thing)
        r = session.scalars(stmt).one_or_none()
        if r is None:
            r = cls(name=thing)
            session.add(r)
            session.commit()
        return r.id


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    @classmethod
    def find_or_insert(cls, session: Session, thing) -> int:
        stmt = select(cls).where(cls.name == thing)
        r = session.scalars(stmt).one_or_none()
        if r is None:
            r = cls(name=thing)
            session.add(r)
            session.commit()
        return r.id


class Films(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"Film(id={self.id!r}, name = {self.name!r})"

    @classmethod
    def find_or_insert(cls, session: Session, thing) -> int:
        stmt = select(cls).where(cls.name == thing)
        r = session.scalars(stmt).one_or_none()
        if r is None:
            r = cls(name=thing)
            session.add(r)
            session.commit()
        return r.id


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    @classmethod
    def find_or_insert(cls, session: Session, thing) -> int:
        stmt = select(cls).where(cls.name == thing)
        r = session.scalars(stmt).one_or_none()
        if r is None:
            r = cls(name=thing)
            session.add(r)
            session.commit()
        return r.id


class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    @classmethod
    def find_or_insert(cls, session: Session, thing) -> int:
        stmt = select(cls).where(cls.name == thing)
        r = session.scalars(stmt).one_or_none()
        if r is None:
            r = cls(name=thing)
            session.add(r)
            session.commit()
        return r.id


class Picks(Base):
    __tablename__ = "picks"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id = {self.id!r}, person = {self.person_id!r},"
            f"pick = {self.pick_id!r}, year = {self.year!r})"
        )


class BookPicks(Picks):
    book_id: Mapped[int | None] = mapped_column(ForeignKey("books.id"))
    pick_id = synonym("book_id")


class FilmPicks(Picks):
    film_id: Mapped[int | None] = mapped_column(ForeignKey("films.id"))
    pick_id = synonym("film_id")


class SeriesPicks(Picks):
    series_id: Mapped[int | None] = mapped_column(ForeignKey("series.id"))
    pick_id = synonym("series_id")


class GamesPicks(Picks):
    game_id: Mapped[int | None] = mapped_column(ForeignKey("games.id"))
    pick_id = synonym("game_id")
