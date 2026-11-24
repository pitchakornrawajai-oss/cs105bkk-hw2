"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from collections import Counter

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got {capacity}")
        if title in self.events:
            raise ValueError(f"event already exists: {title!r}")
        ev = Event(title=title, capacity=capacity)
        self.events[title] = ev
        return ev

    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        try:
            return self.events[title]
        except KeyError as exc:
            raise UnknownEventError(title) from exc
    
    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            return f"Sorry, I don't understand {line!r}."
        action, title, member = parts
        cmd = action.lower()
        if cmd not in {"join", "leave"} or not title or not member:
            return f"Sorry, I don't understand {line!r}."

        try:
            ev = self.event(title)
            if cmd == "join":
                status = ev.sign_up(member)
                if status == "seat":
                    return f"{member} has a seat at {ev.title}."
                return f"{member} is on the waitlist for {ev.title}."
            else:
                promoted = ev.cancel(member)
                if promoted is not None:
                    return f"{member} left {ev.title}. {promoted} gets the seat."
                return f"{member} left {ev.title}."
        except SignupError as exc:
            return f"Sorry, {exc}."

    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        counts: Counter[str] = Counter()
        for ev in self.events.values():
            counts.update(ev.seats)
        return dict(counts)

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
