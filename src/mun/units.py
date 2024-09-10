from __future__ import annotations

from mun.common_units import (
    BaseUnitType,  # noqa: F401
    Gram,
    Hour,
    Kelvin,
    Kilogram,
    KilogramPerMeterCubed,
    Kilometer,
    KilometerSquared,
    KiloUnitType,  # noqa: F401
    Meter,
    MeterCubed,
    MeterPerSecond,
    MeterPerSecondSquared,
    MeterSquared,
    MeterSquaredPerSecond,
    MiliUnitType,  # noqa: F401
    Minute,
    Newton,
    Pascal,
    Second,
    Unit,
    UnitInfo,
    UnitOps,
    UnitType,  # noqa: F401
    registry,  # noqa: F401
)


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
        for id in Registry.units:
            if id.name == symbol:
                unit = Registry.units[id]
                return unit
            elif id.aliases and symbol in id.aliases:
                unit = Registry.units[id]
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Measurement):
            return self.unit == other.unit and self.value == other.value
        elif isinstance(other, float):
            return self.value == other
        else:
            return False

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
