from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from mun.common_units import Meter, Second, UnitId, BaseUnit


@dataclass
class Unit:
    symbol: str
    kind: str
    to_base: Any
    from_base: Any


class Measurement:
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

    def __add__(self, other: Measurement | float) -> Measurement:
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


class Registry:
    """
    A registry that manages unit definitions.
    """

    units: dict[UnitId, Unit] = {
        Meter.id: Unit("m", "length", Meter.to_base, Meter.from_base),
        Second.id: Unit("s", "time", Second.to_base, Second.from_base),
    }

    def add_unit(self, id: UnitId, unit: Unit):
        Registry.units[id] = unit

    @property
    def meter(self) -> Unit:
        return self.units[Meter.id]

    @property
    def second(self) -> Unit:
        return self.units[Second.id]
