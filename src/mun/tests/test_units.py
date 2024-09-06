from mun.units import Inch, Measurement, Meter, Second


def test_convert():
    len1 = Measurement(1.0, Meter)
    assert len1.__str__() == "1.0 m"

    len2 = len1.to(Inch)
    assert len2.unit.symbol == "in"

    len3 = Measurement(1.0, Inch)
    len3.from_(len1)


def test_add():
    len1 = Measurement(1.0, Meter)
    len2 = Measurement(1.0, Meter)

    add = len1 + len2
    assert add.__str__() == "2.0 m"
