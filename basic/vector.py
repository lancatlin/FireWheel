class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError

    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])

    def __mul__(self, value):
        return Vector(self.x * value, self.y * value)

    def __truediv__(self, value):
        return Vector(self.x / value, self.y / value)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.x == other[0]) and (self.y == other[1])
