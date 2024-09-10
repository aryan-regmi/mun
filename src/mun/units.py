from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from mun.common_units import (
    Kelvin,
    Kilometer,
    KilometerSquared,
    MeterCubed,
    MeterPerSecond,
    MeterPerSecondSquared,
    MeterSquared,
    Newton,
    Pascal,
    UnitType,
    BaseUnitType,
    Gram,
    Hour,
    KiloUnitType,
    Kilogram,
    Meter,
    MiliUnitType,
    Minute,
    Second,
    UnitInfo,
)


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


# TODO: Add `to` and `from_` methods
#
# TODO: Add `reduce` and `expand` methods
#
# TODO: Add `__pow__` method
class Measurement[T]:
    """
    Represents a measurement (a value and its unit).

    The unit type can be explicity specifed, but it is only for bookeeping: the
    class doesn't reference it in any way.

    # Note
    Units created by multiplying (`__mul__`) or dividing (`__div__`) units together will not have valid `to_base` and `from_base` methods.
        - To implement that functionality, create a custom unit.
    """

    def __init__(self, value: float, unit: Unit | str):
        """
        Creates a new measurement with the given value and unit.

        # Inputs:
            value   - The actual measurement value.
            unit    - A `Unit`, or a string representing a unit registered in the `Registry`.
        """

        self.value: float = value

        if isinstance(unit, Unit):
            self.unit = unit

        # Match unit to name/aliases in registry
        if isinstance(unit, str):
            for id in Registry.units:
                if id.name == unit:
                    self.unit = Registry.units[id]
                    return
                elif id.aliases and unit in id.aliases:
                    self.unit = Registry.units[id]
                    return

    def __str__(self) -> str:
        if self.unit.symbol:
            return f"{self.value} {self.unit.symbol}"
        else:
            return f"{self.value} {self.unit.__ne__}"

    def __add__(self, other: Measurement | float) -> Measurement[T]:
        if isinstance(other, Measurement):
            if self.unit.kind == other.unit.kind:
                if (
                    self.unit.to_base != None
                    and other.unit.to_base != None
                    and self.unit.from_base
                ):
                    base_value = self.unit.to_base(self.value) + other.unit.to_base(
                        other.value
                    )
                    return Measurement(self.unit.from_base(base_value), self.unit)
                else:
                    raise TypeError(
                        "`self` and `other` must have units with `to_base` and `from_base` methods defined"
                    )
            else:
                raise TypeError(f"`other` must be a unit of {self.unit.kind}")
        else:
            return Measurement(self.value + other, self.unit)

    def __sub__(self, other: Measurement | float) -> Measurement[T]:
        if isinstance(other, Measurement):
            if self.unit.kind == other.unit.kind:
                if (
                    self.unit.to_base != None
                    and other.unit.to_base != None
                    and self.unit.from_base
                ):
                    base_value = self.unit.to_base(self.value) - other.unit.to_base(
                        other.value
                    )
                    return Measurement(self.unit.from_base(base_value), self.unit)
                else:
                    raise TypeError(
                        "`self` and `other` must have units with `to_base` and `from_base` methods defined"
                    )
            else:
                raise TypeError(f"`other` must be a unit of {self.unit.kind}")
        else:
            return Measurement(self.value - other, self.unit)

    def _get_unit(self, symbol: str) -> Unit | None:
        """
        Gets a unit matching the symbol from the registry if one exists.
        """
        for id in Registry.units:
            if id.name == symbol:
                unit = Registry.units[id]
                return unit
            elif id.aliases and symbol in id.aliases:
                unit = Registry.units[id]
                return unit

    def __mul__(self, other: Measurement | float) -> Measurement:
        if isinstance(other, Measurement):
            symbol = self.unit.symbol + "*" + other.unit.symbol
            kind = self.unit.kind + "*" + other.unit.kind
            unit: Unit | None = self._get_unit(symbol)

            # Create new unit if one doesn't exist
            if unit is None:
                unit = Unit(
                    symbol=symbol,
                    kind=kind,
                    to_base=None,
                    from_base=None,
                    components=[self.unit, other.unit],
                    ops=[UnitOps.Mul],
                )

            return Measurement(self.value * other.value, unit)
        else:
            return Measurement(self.value * other, self.unit)

    def __div__(self, other: Measurement | float) -> Measurement:
        if isinstance(other, Measurement):
            symbol = self.unit.symbol + "/" + other.unit.symbol
            kind = self.unit.kind + "/" + other.unit.kind
            unit: Unit | None = self._get_unit(symbol)

            # Create new unit if one doesn't exist
            if unit is None:
                unit = Unit(
                    symbol=symbol,
                    kind=kind,
                    to_base=None,
                    from_base=None,
                    components=[self.unit, other.unit],
                    ops=[UnitOps.Div],
                )

            return Measurement(self.value / other.value, unit)
        else:
            return Measurement(self.value / other, self.unit)

    def __pow__(self, exp: int) -> Measurement:
        symbol = f"{self.unit.symbol}^{exp}"
        unit: Unit | None = self._get_unit(symbol)

        # Create new unit if one doesn't exist
        if unit is None:
            unit = Unit(
                symbol=symbol,
                kind="",
                to_base=None,
                from_base=None,
                components=[self.unit for _ in range(exp)],
                ops=[UnitOps.Div],
            )

        return Measurement(self.value**exp, unit)

    __ladd__ = __add__
    __radd__ = __add__

    __lsub__ = __sub__
    __rsub__ = __sub__

    __lmul__ = __mul__
    __rmul__ = __mul__

    __ldiv__ = __div__
    __rdiv__ = __div__
    __floordiv__ = __div__
    __truediv__ = __div__

    def is_kind(self, kind: str) -> bool:
        """
        Checks if the measurement is the specifed `kind`
        """
        return self.unit.kind == kind


class Registry:
    """
    A registry that manages unit definitions.

    A custom unit can be registered using the `add_unit` method.

    # Note
    Only one registry should be used at a time, and `mun` creates and exports a default
    one in its `__init__.py`; you must import `mun` seperately to use it.
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
    }

    def add_unit(self, id: UnitInfo, unit: Unit):
        """
        Adds a custom unit to the registry.

        # Example
        ```python
        import mun
        from mun import UnitInfo, BaseUnitType

        units = mun.registry

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
    def pascal(self) -> Unit:
        """Represents a Pascal."""
        return self.units[Pascal.id]

    # Temperature
    # ================================================================
    def kelvin(self) -> Unit:
        """Represents a Kelvin."""
        return self.units[Kelvin.id]
