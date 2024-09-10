from __future__ import annotations
from enum import Enum
from typing import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from mun.units import Registry

registry = Registry()


class UnitOps(Enum):
    """Represents an operation between units to create compound units."""

    Mul = 0
    Div = 1


@dataclass
class Unit:
    """
    Represents a unit of measure.

    symbol          - They symbol to display when printing the unit.
    kind            - The kind of measurement (e.g. "length", "time", "mass", etc.)
    to_base         - A function that takes a `float` value and converts it into the
                      base unit.
                      `to_base(value: float) -> float`
    from_base       - A function that takes a `float` value in the base unit and
                      converts it into this unit.
                      `from_base(value: float) -> float`
    components      - The list of `Unit`s that this unit is composed of. Only valid for
                      compound units.
                      This is necessary if you wish to simplify or expand `Measurement`s
                      of compound units.
                      (Defaults to `None`)
    ops             - The list of operations (`UnitOps`) that corresponds to the
                      `components` list.
                      This defines the relationships between the component units;
                      its length must be 1 less than the length of `components`.
                      (Defaults to `None`)
    """

    symbol: str
    kind: str
    to_base: Callable | None
    from_base: Callable | None
    components: list[Unit] | None = None
    ops: list[UnitOps] | None = None


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

    components: list[Unit] = [registry.meter, registry.meter]
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

    components: list[Unit] = [registry.kilometer, registry.kilometer]
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
        registry.meter,
        registry.meter,
        registry.meter,
    ]
    ops: list[UnitOps] = [UnitOps.Mul, UnitOps.Mul]


# Velocity Units
# ================================


class MeterPerSecond(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "meter per second",
        [
            "m/s",
            "mps",
            "metre per second",
            "metres per second",
            "meters per second",
            "Meter Per Second",
            "Metre Per Second",
            "Metres Per Second",
            "Meters Per Second",
        ],
    )

    components: list[Unit] = [
        registry.meter,
        registry.second,
    ]
    ops: list[UnitOps] = [UnitOps.Div]


# Acceleration Units
# ================================


class MeterPerSecondSquared(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "meter per second squared",
        [
            "m/s^2",
            "m/s**2",
            "m/s/s",
            "metre per second squared",
            "metres per second squared",
            "meters per second squared",
            "Meter Per Second Squared",
            "Metre Per Second Squared",
            "Metres Per Second Squared",
            "Meters Per Second Squared",
        ],
    )

    components: list[Unit] = [
        registry.meter,
        registry.second,
        registry.second,
    ]
    ops: list[UnitOps] = [UnitOps.Div, UnitOps.Div]


# Force Units
# ================================


class Newton(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "newton",
        [
            "N",
            "Newton",
            "newtons",
            "Newtons",
            "kg*m/s^2",
            "kg*m/s/s",
            "kg*m/s**2",
        ],
    )

    components: list[Unit] = [
        registry.kilogram,
        registry.meter_per_second_squared,
    ]
    ops: list[UnitOps] = [UnitOps.Mul]


# Pressure Units
# ================================
class Pascal(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "pascal",
        [
            "Pa",
            "Pascal",
            "pascals",
            "Pascals",
            "N/m^2",
            "N/m/m",
            "N/m**2",
        ],
    )

    components: list[Unit] = [
        registry.newton,
        registry.meter_squared,
    ]
    ops: list[UnitOps] = [UnitOps.Div]


# Temperature Units
# ================================
class Kelvin(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "kelvin",
        [
            "K",
            "Kelvin",
            "kelvins",
            "Kelvins",
        ],
    )


# Density Units
# ================================
class KilogramPerMeterCubed(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "kilogram per meter cubed",
        [
            "kg/m^3",
            "kg/m**3",
            "kg/m/m/m",
            "kilograms per meter cubed",
            "Kilogram Per Meter Cubed",
            "Kilograms Per Meter Cubed",
        ],
    )

    components: list[Unit] = [
        registry.kilogram,
        registry.meter_cubed,
    ]
    ops: list[UnitOps] = [UnitOps.Div]


# Viscosity Units
# ================================
class MeterSquaredPerSecond(BaseUnitType):
    id: UnitInfo = UnitInfo(
        "meter squared per second",
        [
            "m^2/s",
            "m**2/s",
            "meters squared per second",
            "metre squared per second",
            "metres squared per second",
            "Meters Squared Per Second",
            "Metre Squared Per Second",
            "Metres Squared Per Second",
        ],
    )

    components: list[Unit] = [
        registry.meter_squared,
        registry.second,
    ]
    ops: list[UnitOps] = [UnitOps.Div]
