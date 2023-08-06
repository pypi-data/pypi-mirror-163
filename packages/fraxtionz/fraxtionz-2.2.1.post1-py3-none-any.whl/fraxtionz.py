"""
Fraxtionz, by Elia Toselli.
A module to manage fractions with precision.
"""

import math


class Fraction(object):
    """
The main fraction class.
    """
    def __init__(self, n, d=1):
        assert isinstance(n, int)
        assert isinstance(d, int)
        if d == 0:
            raise ZeroDivisionError
        div = math.gcd(n, d)
        if div != 1:
            self.n = n // div
            self.d = d // div
        else:
            self.n = n
            self.d = d

    def __str__(self):
        return "{}/{}".format(self.n, self.d)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def lcm(n, m):
        """Calculates the lesser common multiple

:param n: first number
:type n: int

:param m: second number
:type m: int
:return: the lesser common multiple
:rtype: int
"""
        return (n * m) / math.gcd(n, m)

    def lcden(self, other):
        """Calculates the lesser common denominator between two fractions

:param other: second fraction
:type other: Fraction

:return: the lesser common denominator between self and other
:rtype: int
"""
        return Fraction.lcm(self.d, other.d)

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.n * other.d + other.n * self.d,
                            self.d * other.d)
        elif isinstance(other, int):
            other = Fraction(other)
            return Fraction(self.n * other.d + other.n * self.d,
                            self.d * other.d)

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, other):
        return self.n == other.n and self.d == other.d

    def __lt__(self, other):
        return self.n * other.d < self.d * other.n

    def __le__(self, other):
        return self == other or self < other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __mul__(self, other):
        return Fraction(self.n * other.n, self.d * other.d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __invert__(self):
        return Fraction(self.d, self.n)

    def __truediv__(self, other):
        return self.__mul__(other.__invert__())

    def __floordiv__(self, other):
        result = self / other
        return result.n // result.d

    def __rtruediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return other.__truediv__(self)

    def __rfloordiv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return other.__floordiv__(self)

    def __neg__(self):
        return Fraction(0-self.n, self.d)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self + other.__neg__()

    def __rsub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return other + self.__neg__()

    def floatdump(self):
        """ Returns the conventional floating-point value from the fraction """
        return float(self.n / self.d)

    @staticmethod
    def floatofract(num):
        """Transforms a floating-point number into a fraction.

:param num: the floating point number
:type other: float

:return: the fraction
:rtype: Fraction
"""
        while num != float(int(num)):
            num = num * 10
        return Fraction(int(num), int("1" + "0"*len(str(int(num)))))
