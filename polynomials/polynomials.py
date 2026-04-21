from numbers import Number


def derivative(self):
    return self.dx()


class Polynomial:

    def __init__(self, coefs):
        if isinstance(coefs, tuple) or isinstance(coefs, list):
            filled = False
            for x in coefs:
                if x != 0:
                    filled = True
            if not filled:
                coefs = [0]
            if len(coefs) > 1 and filled:
                firsttype = type(coefs)
                coefs = list(coefs)
                for i in range(len(coefs) - 1, -1, -1):
                    if coefs[i] == 0:
                        coefs.pop(i)
                    else:
                        coefs = firsttype(coefs)
                        break
        else:
            coefs = [coefs]
        self.coefficients = tuple(coefs)

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []
        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __sub__(self, other):

        if isinstance(other, Polynomial):
            diff = self.degree() - other.degree()
            selfcoefs = list(self.coefficients)
            othercoefs = list(other.coefficients)
            if diff >= 0:
                multi = 1
                coefs = [selfcoefs, othercoefs]
            else:
                multi = -1
                coefs = [othercoefs, selfcoefs]
            for i in range(0, diff, multi):
                coefs[1].append(0)
            if multi == -1:
                coefs = [coefs[1], coefs[0]]
            newcoefs = []
            i = 0
            for x in coefs[0]:
                newcoefs.append(x - coefs[1][i])
                i += 1
            return Polynomial(newcoefs)
        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            selfcoefs = self.coefficients
            othercoefs = other.coefficients
            newcoefs = [0 for i in range(len(selfcoefs) + len(othercoefs))]
            for i in range(len(selfcoefs)):
                for j in range(len(othercoefs)):
                    newcoefs[i + j] = (newcoefs[i + j] +
                                       selfcoefs[i]*othercoefs[j])
        if isinstance(other, Number):
            newcoefs = tuple(x*other for x in self.coefficients)
        return Polynomial(newcoefs)

    def __pow__(self, other):
        newpoly = self
        for i in range(1, other):
            newpoly *= self
        return newpoly

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        negativecoefs = tuple(-1*x for x in self.coefficients)
        return Polynomial(negativecoefs) + other

    def __rmul__(self, other):
        return self * other

    def __call__(self, other):
        total = 0
        i = 0
        for x in self.coefficients:
            total += x*(other**i)
            i += 1
        return total

    def dx(self):
        i = 0
        newcoefs = []
        for x in self.coefficients:
            newcoefs.append(x*i)
            i += 1
        newcoefs.pop(0)
        return Polynomial(newcoefs)
