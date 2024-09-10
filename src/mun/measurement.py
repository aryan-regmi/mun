from __future__ import annotations
from mun.units import Unit, UnitOps, ureg


# TODO: Add `to` and `from_` methods
#
# TODO: Add `reduce` and `expand` methods
class Measurement[T]:
    """
    Represents a measurement (a value and its unit).

    The unit type can be explicity specifed, but it is only for bookeeping: the
    class doesn't reference it in any way.

    # Note
    Units created by multiplying (`__mul__`) or dividing (`__div__`) units together will not have valid `to_base` and `from_base` methods.
        - To implement that functionality, create a custom unit.
    """

    def from_[U](self, measurement: Measurement[U]) -> Measurement[T]:
        """
        Creates a new measurement from the given one.

        # Note
        This does not check if `U` can be converted into `T`, and simply assigns its
        value to the returned measurement.
        """
        return Measurement(measurement.value, self.unit)

    # TODO: incorporate `from_` into `__init__`
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
            for id in ureg.units:
                if id.name == unit:
                    self.unit = ureg.units[id]
                    return
                elif id.aliases and unit in id.aliases:
                    self.unit = ureg.units[id]
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
                    self.unit.to_base is not None
                    and other.unit.to_base is not None
                    and self.unit.from_base
                ):
                    base_value = self.unit.to_base(self.value) + other.unit.to_base(  # type: ignore
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
                    self.unit.to_base is not None
                    and other.unit.to_base is not None
                    and self.unit.from_base
                ):
                    base_value = self.unit.to_base(self.value) - other.unit.to_base(  # type: ignore
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

    def _get_unit(self, symbol: str) -> Unit | None:  # type: ignore
        """
        Gets a unit matching the symbol from the registry if one exists.
        """
        for id in ureg.units:
            if id.name == symbol:
                unit = ureg.units[id]
                return unit
            elif id.aliases and symbol in id.aliases:
                unit = ureg.units[id]
                return unit
            else:
                return None

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
                    components=[self.unit.symbol, other.unit.symbol],
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
                    components=[self.unit.symbol, other.unit.symbol],
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
                components=[self.unit.symbol for _ in range(exp)],
                ops=[UnitOps.Div],
            )

        return Measurement(self.value**exp, unit)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value == other.value
        elif isinstance(other, float):
            return self.value == other
        else:
            raise TypeError("`other` must be `Measurement` or `float`")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Measurement):
            return self.unit != other.unit or self.value != other.value
        elif isinstance(other, float):
            return self.value != other
        else:
            raise TypeError("`other` must be `Measurement` or `float`")

    def __gt__(self, other: Measurement | float) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other: Measurement | float) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value >= other.value
        else:
            return self.value >= other

    def __lt__(self, other: Measurement | float) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value < other.value
        else:
            return self.value < other

    def __le__(self, other: Measurement | float) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value <= other.value
        else:
            return self.value <= other

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
