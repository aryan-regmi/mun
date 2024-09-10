from __future__ import annotations
from enum import Enum
from typing import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override


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
    components: list[str] | None = None
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

    components: list[str] = ["m", "m"]
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

    components: list[str] = ["km", "km"]
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

    components: list[str] = [
        "m",
        "m",
        "m",
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

    components: list[str] = [
        "m",
        "s",
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

    components: list[str] = [
        "m",
        "s",
        "s",
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

    components: list[str] = [
        "kg",
        "m/s^2",
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

    components: list[str] = [
        "N",
        "m^2",
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

    components: list[str] = [
        "kg",
        "m^3",
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

    components: list[str] = [
        "m^2",
        "s",
    ]
    ops: list[UnitOps] = [UnitOps.Div]


class Registry:
    """
    A registry that manages unit definitions.

    A custom unit can be registered using the `add_unit` method.

    # Note
    Only one registry should be used at a time.
    """

    # The registered units
    units: dict[UnitInfo, Unit] = {
        # Length
        Meter.id: Unit("m", "length", Meter.to_base, Meter.from_base),
        Kilometer.id: Unit("km", "length", Kilometer.to_base, Kilometer.from_base),
        # Time
        Second.id: Unit("s", "time", Second.to_base, Second.from_base),
        Minute.id: Unit("min", "time", Minute.to_base, Minute.from_base),
        Hour.id: Unit("hr", "time", Hour.to_base, Hour.from_base),
        # Mass
        Gram.id: Unit("g", "mass", Gram.to_base, Gram.from_base),
        Kilogram.id: Unit("kg", "mass", Kilogram.to_base, Kilogram.from_base),
        # Area
        MeterSquared.id: Unit(
            "m^2", "area", MeterSquared.to_base, MeterSquared.from_base
        ),
        KilometerSquared.id: Unit(
            "km^2", "area", KilometerSquared.to_base, KilometerSquared.from_base
        ),
        # Volume
        MeterCubed.id: Unit("m^3", "volume", MeterCubed.to_base, MeterCubed.from_base),
        # Velocity
        MeterPerSecond.id: Unit(
            "m/s", "velocity", MeterPerSecond.to_base, MeterPerSecond.from_base
        ),
        # Acceleration
        MeterPerSecondSquared.id: Unit(
            "m/s^2",
            "acceleration",
            MeterPerSecondSquared.to_base,
            MeterPerSecondSquared.from_base,
        ),
        # Force
        Newton.id: Unit("N", "force", Newton.to_base, Newton.from_base),
        # Pressure
        Pascal.id: Unit("Pa", "pressure", Pascal.to_base, Pascal.from_base),
        # Temperature
        Kelvin.id: Unit("K", "temperature", Kelvin.to_base, Kelvin.from_base),
        # Density
        KilogramPerMeterCubed.id: Unit(
            "kg/m^3",
            "density",
            KilogramPerMeterCubed.to_base,
            KilogramPerMeterCubed.from_base,
        ),
        # Viscosity
        MeterSquaredPerSecond.id: Unit(
            "m^2/s",
            "viscosity",
            MeterSquaredPerSecond.to_base,
            MeterSquaredPerSecond.from_base,
        ),
    }

    def add_unit(self, id: UnitInfo, unit: Unit):
        """
        Adds a custom unit to the registry.

        # Example
        ```python
        import mun
        from mun import UnitInfo, BaseUnitType

        units = mun.Registry()

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

        units.add_unit(Meter.id, Unit("m", "length", Meter.to_base, Meter.from_base))
        ```
        """
        Registry.units[id] = unit

    # Length
    # ================================================================
    @property
    def meter(self) -> Unit:
        """Represents a meter."""
        return self.units[Meter.id]

    @property
    def kilometer(self) -> Unit:
        """Represents a Kilometer."""
        return self.units[Kilometer.id]

    # Time
    # ================================================================
    @property
    def second(self) -> Unit:
        """Represents a second."""
        return self.units[Second.id]

    @property
    def minute(self) -> Unit:
        """Represents a minute."""
        return self.units[Minute.id]

    @property
    def hour(self) -> Unit:
        """Represents an hour."""
        return self.units[Hour.id]

    # Mass
    # ================================================================
    @property
    def gram(self) -> Unit:
        """Represents a gram."""
        return self.units[Gram.id]

    @property
    def kilogram(self) -> Unit:
        """Represents a kilogram."""
        return self.units[Kilogram.id]

    # Area
    # ================================================================
    @property
    def meter_squared(self) -> Unit:
        """Represents a `m^2`."""
        return self.units[MeterSquared.id]

    @property
    def kilometer_squared(self) -> Unit:
        """Represents a `km^2`."""
        return self.units[KilometerSquared.id]

    # Volume
    # ================================================================
    @property
    def meter_cubed(self) -> Unit:
        """Represents a `m^3`."""
        return self.units[MeterCubed.id]

    # Velocity
    # ================================================================
    @property
    def meter_per_second(self) -> Unit:
        """Represents a `m/s`."""
        return self.units[MeterPerSecond.id]

    # Acceleration
    # ================================================================
    @property
    def meter_per_second_squared(self) -> Unit:
        """Represents a `m/s^2`."""
        return self.units[MeterPerSecondSquared.id]

    # Force
    # ================================================================
    @property
    def newton(self) -> Unit:
        """Represents a Newton."""
        return self.units[Newton.id]

    # Pressure
    # ================================================================
    @property
    def pascal(self) -> Unit:
        """Represents a Pascal."""
        return self.units[Pascal.id]

    # Temperature
    # ================================================================
    @property
    def kelvin(self) -> Unit:
        """Represents a Kelvin."""
        return self.units[Kelvin.id]

    # Density
    # ================================================================
    @property
    def kilogram_per_meter_cubed(self) -> Unit:
        """Represents a `kg/m^3`."""
        return self.units[KilogramPerMeterCubed.id]

    # Viscosity
    # ================================================================
    @property
    def meter_squared_per_second(self) -> Unit:
        """Represents a `m^2/s`."""
        return self.units[MeterSquaredPerSecond.id]


ureg = Registry()
