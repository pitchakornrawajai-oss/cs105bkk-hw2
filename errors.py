"""HW2 · errors.py: the club's own exceptions. Practises Session 6: custom exception classes
that share one parent and carry the details for whoever catches them."""


class SignupError(Exception):
    """Base error for sign-up problems."""


class NotSignedUpError(SignupError):
    """Raised when a member is not signed up for an event."""

    def __init__(self, member, event):
        super().__init__(f"{member} is not signed up for {event}")
        self.member = member
        self.event = event


class AlreadySignedUpError(SignupError):
    """Raised when a member is already on seats or waitlist."""

    def __init__(self, member, event):
        super().__init__(f"{member} is already signed up for {event}")
        self.member = member
        self.event = event


class UnknownEventError(SignupError):
    """Raised when no event matches the given title."""

    def __init__(self, title):
        super().__init__(f"there is no event called {title!r}")
        self.title = title