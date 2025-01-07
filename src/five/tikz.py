from sqlalchemy import select, func
from .tables import People


class Graph:
    people: dict[int, str]
    pick_items: dict[int, int]
    picks: list[tuple[int, int]]
    year: int

    def __init__(self, session, table, pick_table):
        current_year = session.scalar(select(func.max(pick_table.year)))
        stmt = (
            select(pick_table)
            .where(pick_table.year == current_year)
            .where(pick_table.pick_id.is_not(None))
        )
        current_picks = session.scalars(stmt).all()

        self.picks = list()

        current_pick_ids = {p.pick_id for p in current_picks}
        for p in current_picks:
            self.pick_items[p.pick_id] = session.scalar(
                select(table.name).where(table.id == p.pick_id)
            )
            self.picks.append((p.pick_id, p.person_id))

        stmt = (
            select(pick_table)
            .where(pick_table.year < current_year)
            .where(pick_table.pick_id.in_(current_pick_ids))
        )
        past_picks = session.scalars(stmt).all()
        self.past_picks = list()
        for p in past_picks:
            self.past_picks.append((p.pick_id, p.person_id))

        people_ids = {p.person_id for p in current_picks + past_picks}
        for p in people_ids:
            self.people[p] = session.scalar(select(People.name).where(People.id == p))


def graph_tikz_from_sql(session, table, pick_table) -> str:
    tex = [
        r"\documentclass[tikz]{standalone}",
        r"\usetikzlibrary{graphs,graphdrawing}",
        r"\usegdlibrary{force}",
        r"\begin{document}",
        r"\tikzset{past/.style={opacity=0.1}}",
    ]
    tikz = [
        r"\tikz[spring electrical layout,",
        r"electric force order=2,",
        r"node distance=3cm,",
        r"align=center,",
        r"]{",
    ]

    current_year = session.scalar(select(func.max(pick_table.year)))

    # Get all pick table mappings
    stmt = (
        select(pick_table)
        .where(pick_table.year == current_year)
        .where(pick_table.pick_id.is_not(None))
    )
    current_picks = session.scalars(stmt).all()

    # Gather all pick_ids
    current_pick_ids = {p.pick_id for p in current_picks}
    # Look for past matches
    stmt = (
        select(pick_table)
        .where(pick_table.year < current_year)
        .where(pick_table.pick_id.in_(current_pick_ids))
    )
    past_picks = session.scalars(stmt).all()

    # Make people nodes
    people_ids = {p.person_id for p in current_picks + past_picks}
    tikz_people_nodes = []
    for p in people_ids:
        name = session.scalar(select(People.name).where(People.id == p))
        s = r"\node (" + str("pers" + str(p)) + r") {\textbf{" + str(name) + r"}};"
        tikz_people_nodes.append(s)

    # Make pick nodes
    tikz_pick_nodes = []
    for p in current_pick_ids:
        name = session.scalar(select(table.name).where(table.id == p))
        s = r"\node (" + str("pick" + str(p)) + r") {" + str(name) + r"};"
        tikz_pick_nodes.append(s)

    # Join current picks
    tikz_current_link_nodes = [r"\draw "]
    for p in current_picks:
        s = f"({'pers' + str(p.person_id)}) edge ({'pick' + str(p.pick_id)})"
        tikz_current_link_nodes.append(s)
    tikz_current_link_nodes.append(r";")

    # Join previous picks
    tikz_past_link_nodes = [r"\draw [past] "]
    for p in past_picks:
        s = f"({'pers' + str(p.person_id)}) edge ({'pick' + str(p.pick_id)})"
        tikz_past_link_nodes.append(s)
    tikz_past_link_nodes.append(r";")

    tikz = (
        tikz
        + tikz_people_nodes
        + tikz_pick_nodes
        + tikz_current_link_nodes
        + tikz_past_link_nodes
        + [r"}"]
    )
    return "\n".join(tex + tikz + [r"\end{document}"])
