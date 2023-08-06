from neighborly.core.status import Status
from neighborly.core.time import SimDateTime


class Child(Status):
    def __init__(self) -> None:
        super().__init__(
            "child",
            "Character is seen as a child in the eyes of society",
        )


class Teen(Status):
    def __init__(self) -> None:
        super().__init__(
            "Adolescent",
            "Character is seen as an adolescent in the eyes of society",
        )


class YoungAdult(Status):
    def __init__(self) -> None:
        super().__init__(
            "Young Adult",
            "Character is seen as a young adult in the eyes of society",
        )


class Adult(Status):
    def __init__(self) -> None:
        super().__init__(
            "Adult",
            "Character is seen as an adult in the eyes of society",
        )


class Elder(Status):
    def __init__(self) -> None:
        super().__init__(
            "Senior",
            "Character is seen as a senior in the eyes of society",
        )


class Deceased(Status):
    def __init__(self) -> None:
        super().__init__(
            "Deceased",
            "This character is dead",
        )


class Retired(Status):
    def __init__(self) -> None:
        super().__init__(
            "Retired",
            "This character retired from their last occupation",
        )


class Dependent(Status):
    def __init__(self) -> None:
        super().__init__("Dependent", "This character is dependent on their parents")


class Unemployed(Status):
    __slots__ = "duration_days"

    def __init__(self) -> None:
        super().__init__(
            "Unemployed",
            "Character doesn't have a job",
        )
        self.duration_days: float = 0


class Dating(Status):
    __slots__ = "duration_years", "partner_id", "partner_name"

    def __init__(self, partner_id: int, partner_name: str) -> None:
        super().__init__(
            "Dating",
            "This character is in a relationship with another",
        )
        self.duration_years: float = 0.0
        self.partner_id: int = partner_id
        self.partner_name: str = partner_name

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))
        self.gameobject.world.get_gameobject(self.partner_id).remove_component(
            type(self)
        )


class Married(Status):
    __slots__ = "duration_years", "partner_id", "partner_name"

    def __init__(self, partner_id: int, partner_name: str) -> None:
        super().__init__(
            "Married",
            "This character is married to another",
        )
        self.duration_years = 0.0
        self.partner_id: int = partner_id
        self.partner_name: str = partner_name

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))
        self.gameobject.world.get_gameobject(self.partner_id).remove_component(
            type(self)
        )


class InRelationship(Status):
    __slots__ = "duration_years", "partner_id", "partner_name", "relationship_type"

    def __init__(
        self, relationship_type: str, partner_id: int, partner_name: str
    ) -> None:
        super().__init__(
            "Married",
            "This character is married to another",
        )
        self.relationship_type: str = relationship_type
        self.duration_years = 0.0
        self.partner_id: int = partner_id
        self.partner_name: str = partner_name

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))
        self.gameobject.world.get_gameobject(self.partner_id).remove_component(
            type(self)
        )


class BusinessOwner(Status):
    __slots__ = "duration", "business_id", "business_name"

    def __init__(self, business_id: int, business_name: str) -> None:
        super().__init__(
            "Business Owner",
            "This character owns a business",
        )
        self.duration = 0.0
        self.business_id: int = business_id
        self.business_name: str = business_name

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))


class Pregnant(Status):
    def __init__(
        self, partner_name: str, partner_id: int, due_date: SimDateTime
    ) -> None:
        super().__init__("Pregnant", "This character is pregnant")
        self.partner_name: str = partner_name
        self.partner_id: int = partner_id
        self.due_date: SimDateTime = due_date

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))


class Male(Status):
    def __init__(self):
        super().__init__("Male", "This character is perceived as masculine.")


class Female(Status):
    def __init__(self):
        super().__init__("Female", "This character is perceived as feminine.")


class NonBinary(Status):
    def __init__(self):
        super().__init__("NonBinary", "This character is perceived as non-binary.")


class CollegeGraduate(Status):
    def __init__(self) -> None:
        super().__init__("College Graduate", "This character graduated from college.")


class InTheWorkforce(Status):
    def __init__(self) -> None:
        super().__init__(
            "In the Workforce",
            "This Character is eligible for employment opportunities.",
        )

    def on_archive(self) -> None:
        """Remove status on this character and the partner"""
        self.gameobject.remove_component(type(self))
