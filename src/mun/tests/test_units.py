from mun.units import BaseUnitType, Unit, Measurement, Registry, UnitId

units = Registry()


def test_create():
    len1 = Measurement(1.0, units.meter)
    assert len1.__str__() == "1.0 m"

    len2 = Measurement(1.0, "m")
    assert len2.__str__() == "1.0 m"

    # Custom units
    m2 = Unit("m^2", "area", BaseUnitType.to_base, BaseUnitType.from_base)
    units.add_unit(UnitId("meters squared", ["m2", "m^2"]), m2)

    area = Measurement(1.0, "m2")
    assert area.__str__() == "1.0 m^2"


# TODO: Add tests for rest of arithmetic (sub and div)


def test_add():
    len1 = Measurement(1.0, units.meter)
    len2 = Measurement(1.0, "m")

    add = len1 + len2
    assert add.__str__() == "2.0 m"

    area1 = Measurement(1.0, "m2")
    area2 = Measurement(1.0, "m2")

    add = area1 + area2
    assert add.__str__() == "2.0 m^2"

    add = area1 + 1
    assert add.__str__() == "2.0 m^2"

    add = 1 + area1
    assert add.__str__() == "2.0 m^2"


def test_mul():
    len1 = Measurement(1.0, units.meter)
    len2 = Measurement(1.0, "m")

    mul = len1 * len2
    assert mul.__str__() == "1.0 m*m"

    area1 = Measurement(1.0, "m2")
    mul = area1 * len1
    assert mul.__str__() == "1.0 m^2*m"

    mul = area1 * 1.0
    assert mul.__str__() == "1.0 m^2"

    mul = 1.0 * area1
    assert mul.__str__() == "1.0 m^2"
