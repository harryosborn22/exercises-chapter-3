class Circle:

    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self, other):
        diff = ((other[0] - self.centre[0])**2 +
                (other[1] - self.centre[1])**2)**0.5
        return diff < self.radius
