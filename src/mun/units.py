from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from mun.common_units import (
    BaseUnitType,
    Gram,
    Hour,
    KiloUnitType,
    Kilogram,
    Meter,
    MiliUnitType,
    Minute,
    Second,
    UnitId,
)

# TODO: Add `reduce` method to Measurement to simplify units!


@dataclass
class Unit:
    symbol: str
    kind: str
    to_base: Any
    from_base: Any


class Measurement[T]:
    def __init__(self, value: float, unit: Unit | str):
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
                base_value = self.unit.to_base(self.value) + other.unit.to_base(
                    other.value
                )
                return Measurement(self.unit.from_base(base_value), self.unit)
            else:
                raise TypeError(f"`other` must be a unit of {self.unit.kind}")
        else:
            return Measurement(self.value + other, self.unit)

    def __sub__(self, other: Measurement | float) -> Measurement[T]:
        if isinstance(other, Measurement):
            if self.unit.kind == other.unit.kind:
                base_value = self.unit.to_base(self.value) - other.unit.to_base(
                    other.value
                )
                return Measurement(self.unit.from_base(base_value), self.unit)
            else:
                raise TypeError(f"`other` must be a unit of {self.unit.kind}")
        else:
            return Measurement(self.value - other, self.unit)

    def __mul__(self, other: Measurement | float) -> Measurement:
        if isinstance(other, Measurement):
            symbol = self.unit.symbol + "*" + other.unit.symbol
            kind = self.unit.kind + "*" + other.unit.kind
            unit: Unit | None = None

            # Reuse existing unit if available
            for id in Registry.units:
                if id.name == symbol:
                    unit = Registry.units[id]
                    break
                elif id.aliases and symbol in id.aliases:
                    unit = Registry.units[id]
                    break

            # Create new unit if one doesn't exist
            if unit is None:
                unit = Unit(
                    symbol=symbol,
                    kind=kind,
                    to_base=None,
                    from_base=None,
                )

            return Measurement(self.value * other.value, unit)
        else:
            return Measurement(self.value * other, self.unit)

    def __div__(self, other: Measurement | float) -> Measurement:
        if isinstance(other, Measurement):
            symbol = self.unit.symbol + "/" + other.unit.symbol
            kind = self.unit.kind + "/" + other.unit.kind
            unit: Unit | None = None

            # Reuse existing unit if available
            for id in Registry.units:
                if id.name == symbol:
                    unit = Registry.units[id]
                    break
                elif id.aliases and symbol in id.aliases:
                    unit = Registry.units[id]
                    break

            # Create new unit if one doesn't exist
            if unit is None:
                unit = Unit(
                    symbol=symbol,
                    kind=kind,
                    to_base=None,
                    from_base=None,
                )

            return Measurement(self.value / other.value, unit)
        else:
            return Measurement(self.value / other, self.unit)

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


class Registry:
    """
    A registry that manages unit definitions.
    """

    units: dict[UnitId, Unit] = {
        # Length
        Meter.id: Unit("m", "length", Meter.to_base, Meter.from_base),
        # Time
        Second.id: Unit("s", "time", Second.to_base, Second.from_base),
        Minute.id: Unit("min", "time", Minute.to_base, Minute.from_base),
        Hour.id: Unit("hr", "time", Hour.to_base, Hour.from_base),
        # Mass
        Gram.id: Unit("g", "mass", Gram.to_base, Gram.from_base),
        Kilogram.id: Unit("kg", "mass", Kilogram.to_base, Kilogram.from_base),
    }

    def add_unit(self, id: UnitId, unit: Unit):
        Registry.units[id] = unit

    @property
    def meter(self) -> Unit:
        return self.units[Meter.id]

    @property
    def second(self) -> Unit:
        return self.units[Second.id]
