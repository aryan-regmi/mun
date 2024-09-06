from dataclasses import dataclass


@dataclass
class UnitId:
    name: str
    aliases: list[str] | None = None

    def __hash__(self) -> int:
        return hash(self.name)


# Generic Units
# ================================


class BaseUnit:
    @staticmethod
    def to_base(value: float) -> float:
        return value

    @staticmethod
    def from_base(value: float) -> float:
        return value


# Length Units
# ================================


class Meter(BaseUnit):
    id: UnitId = UnitId(
        "meter",
        [
            "m",
            "meters",
            "metre",
            "metres",
            "Meter",
            "Meters",
            "Metre",
            "Metres",
        ],
    )


# Time Units
# ================================


class Second(BaseUnit):
    id: UnitId = UnitId(
        "second",
        [
            "s",
            "sec",
            "secs",
            "seconds",
            "Sec",
            "Secs",
            "Second",
            "Seconds",
        ],
    )
