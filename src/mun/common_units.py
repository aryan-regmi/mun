from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

import mun
from mun import units
from mun.units import Unit, UnitOps  # type: ignore


@dataclass
class UnitInfo:
    """Describes a unit's name and aliases."""

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
    id: UnitInfo = UnitInfo(
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


class Kilometer(KiloUnitType):
    id: UnitInfo = UnitInfo(
        "kilometer",
        [
            "kg",
            "kilometers",
            "Kilometer",
            "Kilometers",
            "kilometres",
            "Kilometre",
            "Kilometres",
        ],
    )


# Time Units
# ================================


class Second(BaseUnitType):
    id: UnitInfo = UnitInfo(
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
    id: UnitInfo = UnitInfo(
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
    id: UnitInfo = UnitInfo(
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
    id: UnitInfo = UnitInfo(
        "gram",
        [
            "g",
            "grams",
            "Gram",
            "Grams",
        ],
    )


class Kilogram(KiloUnitType):
    id: UnitInfo = UnitInfo(
        "kilogram",
        [
            "kg",
            "kilograms",
            "Kilogram",
            "Kilograms",
        ],
    )


# Area Units
# ================================


class MeterSquared(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "meter squared",
        [
            "m*m",
            "m^2",
            "m**2",
            "meters squared",
            "metre squared",
            "metres squared",
            "Meters Squared",
            "Metre Squared",
            "Metres Squared",
        ],
    )

    components: list[Unit] = [mun.registry.meter, mun.registry.meter]
    ops: list[UnitOps] = [UnitOps.Mul]


class KilometerSquared(KiloUnitType):
    id: UnitInfo = UnitInfo(
        "kilometer squared",
        [
            "km*km",
            "km^2",
            "km**2",
            "kilometers squared",
            "kilometre squared",
            "kilometres squared",
            "Kilometers Squared",
            "Kilometre Squared",
            "Kilometres Squared",
        ],
    )

    components: list[Unit] = [mun.registry.kilometer, mun.registry.kilometer]
    ops: list[UnitOps] = [UnitOps.Mul]


# Volume Units
# ================================


class MeterCubed(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "meter cubed",
        [
            "m*m*m",
            "m^3",
            "m**3",
            "meters cubed",
            "metre cubed",
            "metres cubed",
            "Meters Cubed",
            "Metre Cubed",
            "Metres Cubed",
        ],
    )

    components: list[Unit] = [
        mun.registry.meter,
        mun.registry.meter,
        mun.registry.meter,
    ]
    ops: list[UnitOps] = [UnitOps.Mul, UnitOps.Mul]
