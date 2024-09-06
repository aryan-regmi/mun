from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override  # type: ignore


@dataclass
class UnitId:
    name: str
    aliases: list[str] | None = None

    def __hash__(self) -> int:
        return hash(self.name)


# Generic Units
# ================================


class UnitType(ABC):
    @staticmethod
    @abstractmethod
    def to_base(value: float) -> float:
        return value

    @staticmethod
    @abstractmethod
    def from_base(value: float) -> float:
        return value


class BaseUnitType(UnitType):
    @override
    @staticmethod
    def to_base(value: float) -> float:
        return value

    @override
    @staticmethod
    def from_base(value: float) -> float:
        return value


class KiloUnitType(UnitType):
    @override
    @staticmethod
    def to_base(value: float) -> float:
        return value * 1000

    @override
    @staticmethod
    def from_base(value: float) -> float:
        return value / 1000


class MiliUnitType(UnitType):
    @override
    @staticmethod
    def to_base(value: float) -> float:
        return value / 1000

    @override
    @staticmethod
    def from_base(value: float) -> float:
        return value * 1000


# Length Units
# ================================


class Meter(BaseUnitType):
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


class Second(BaseUnitType):
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


class Minute(UnitType):
    id: UnitId = UnitId(
        "minute",
        [
            "min",
            "mins",
            "minutes",
            "Min",
            "Mins",
            "Minutes",
        ],
    )

    @override
    @staticmethod
    def to_base(value: float) -> float:
        return value * 60

    @override
    @staticmethod
    def from_base(value: float) -> float:
        return value / 60


class Hour(UnitType):
    id: UnitId = UnitId(
        "hour",
        [
            "h",
            "hr",
            "hrs",
            "hours",
            "Hour",
            "Hours",
        ],
    )

    @override
    @staticmethod
    def to_base(value: float) -> float:
        return value * 3600

    @override
    @staticmethod
    def from_base(value: float) -> float:
        return value / 3600


# Mass Units
# ================================


class Gram(BaseUnitType):
    id: UnitId = UnitId(
        "gram",
        [
            "g",
            "grams",
            "Gram",
            "Grams",
        ],
    )


class Kilogram(KiloUnitType):
    id: UnitId = UnitId(
        "kilogram",
        [
            "kg",
            "kilograms",
            "Kilogram",
            "Kilograms",
        ],
    )
