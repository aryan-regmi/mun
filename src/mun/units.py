from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class Unit(Protocol):
    name: str
    symbol: str | None
    kind: str

    @staticmethod
    def to_base(value: float) -> float: ...

    @staticmethod
    def from_base(value: float) -> float: ...


class Measurement[T]:
    def __init__(self, value: float, unit: T):
        if isinstance(unit, Unit):
            self.value = value
            self.unit = unit
        else:
            raise TypeError("`unit` must implement the `Unit` protocol")

    def __str__(self) -> str:
        name = self.unit.name
        symbol = self.unit.symbol
        if symbol:
            return f"{self.value} {symbol}"
        else:
            return f"{self.value} {name}"

    def to[U: type](self, unit: U) -> Measurement[U]:
        if isinstance(unit, Unit):
            if self.unit.kind == unit.kind:
                base_value = self.unit.to_base(self.value)
                converted = unit.from_base(base_value)
                return Measurement(converted, unit)
            else:
                raise TypeError(f"`unit` must be a unit of {self.unit.kind}")
        else:
            raise TypeError("`unit` must implement the `Unit` protocol")

    def from_[U](self, value: Measurement[U]):
        if self.unit.kind == value.unit.kind:
            base_value = value.unit.to_base(value.value)
            converted = self.unit.from_base(base_value)
            self.value = converted
        else:
            raise TypeError(f"`value` must have a unit of {self.unit.kind}")

    def __add__[U: type](self, other: Measurement[U] | float) -> Measurement[T]:
        if isinstance(other, Measurement):
            if self.unit.kind == other.unit.kind:
                base_value = self.unit.to_base(self.value) + other.unit.to_base(
                    other.value
                )
                converted = self.unit.from_base(base_value)
                return Measurement(converted, self.unit)
            else:
                raise TypeError(f"`other` must have a unit of {self.unit.kind}")
        else:
            return Measurement(self.value + other, self.unit)


# Time Units
# =================================


class Second:
    name: str = "second"
    symbol: str | None = "s"
    kind: str = "time"

    @staticmethod
    def to_base(value: float) -> float:
        return value

    @staticmethod
    def from_base(value: float) -> float:
        return value


# Length Units
# =================================


class Meter:
    name: str = "meter"
    symbol: str | None = "m"
    kind: str = "length"

    @staticmethod
    def to_base(value: float) -> float:
        return value

    @staticmethod
    def from_base(value: float) -> float:
        return value


class Inch:
    name: str = "inch"
    symbol: str | None = "in"
    kind: str = "length"

    @staticmethod
    def to_base(value: float) -> float:
        return value * 0.0254

    @staticmethod
    def from_base(value: float) -> float:
        return value / 0.0254
