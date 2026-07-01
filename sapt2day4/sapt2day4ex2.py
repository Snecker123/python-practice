"""2. Model the following:
a) a Point class that has two values, x and y, representing coordinates
Add suport for the following
- addition and substraction of two points
- equality
- string representation
Make examples showcasing these capabilities

b) a PointCollection class that has a list of points
Add support for the following
- check that a point is in the collection
- len support
- comparison between two point collections (based on length)
- addition and substraction (for both Point and PointCollection)
- string representation
Make examples showcasing these capabilities

c) a Triangle class that has 3 Point objects representing the corners of the triangle
Add support for the following
- validate that the points form a valid triangle (not a line)
- equality
- string representation
- len support (based on triangle area)
- comparison between other triangles (based on triangle area)
- in support (a triangle is within another triangle, a point is in the triangle, a point collection is in a triangle)

d) a Rectangle class that has 4 Point obejcts representing the corners of the rectangle
Add support for the following
- validate that the points form a valid rectangle
- equality
- string representation
- len support (based on rectangle area)
- comparison between other rectangles (based on rectangle area)
- in support  (a rectangle is within another rectangle, a point is in the rectangle, a point collection is in a rectangle)
"""
from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __add__(self, other) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


    def __str__(self):
        return f"x: {self.x}, y: {self.y}\n"

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}\n"




class PointCollection:
    def __init__(self, collection= None) -> None:
        if collection is None:
            self.collection = []
        else:
            self.collection = collection



    def is_in_collection(self, point: Point) -> bool:
        return point in self.collection


    def __len__(self) -> int:
        return len(self.collection)


    def __gt__(self, other):
        return len(self) > len(other)
    def __ge__(self, other) -> bool:
        return len(self) >= len(other)
    def __lt__(self, other):
        return len(self) < len(other)
    def __le__(self, other):
        return len(self) <= len(other)
    def __eq__(self, other):
        return len(self) == len(other)
    def __ne__(self, other):
        return len(self) != len(other)


    def __add__(self, other) -> PointCollection:
        pc = PointCollection()
        if self > other:
            for i in range(0, len(other)):
                pc.collection.append(other.collection[i] + self.collection[i])
        else:
            for i in range(0, len(self)):
                pc.collection.append(other  .collection[i] + self.collection[i])

        return pc


    def __sub__(self, other) -> PointCollection:
        pc = PointCollection()
        if self > other:
            for i in range(0, len(other)):
                pc.collection.append(self.collection[i] - other.collection[i])
        else:
            for i in range(0, len(self)):
                pc.collection.append(self.collection[i] - other.collection[i])

        return pc

    def __str__(self):
        return f"collection: {self.collection}\n"



p1 = Point(0, 0)
p2 = Point(1, 0)
p3 = Point(2, 0)

col1 = PointCollection([p1, p2, p3])
print(col1.is_in_collection(p1))
print(col1)


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3


    def is_triangle(self) -> bool:
        d1 = sqrt((self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2 )
        d2 = sqrt((self.p3.x - self.p2.x)**2 + (self.p3.y - self.p2.y)**2 )
        d3 = sqrt((self.p3.x - self.p1.x)**2 + (self.p3.y - self.p1.y)**2 )

        if
