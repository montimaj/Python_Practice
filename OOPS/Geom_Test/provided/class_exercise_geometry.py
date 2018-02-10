try:
    from pylab import *
except ImportError:
    print('Could not import the PyLab module')

import math

class Point:
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "Point(%g, %g)" % (self.x, self.y)
    
    def distance(self, obj):
        if isinstance(obj, Point):
            return math.hypot(self.x - obj.x, self.y - obj.y)
        elif isinstance(obj, Rectangle):
            return obj.distance(self)
        return None

    def plot(self, name=None):
        plot([self.x], [self.y], 'o')
        if name:
            text(self.x, self.y, name)
        else:
            text(self.x, self.y, self.__str__())

class Rectangle:
    width = 0
    height = 0
    corner = None
    
    def __init__(self, p, w, h):
        self.corner, self.width, self.height = p, w, h

    def __str__(self):
        return "Rectangle(%s, %g, %g)" % (self.corner.__str__(), self.width, self.height)
    
    def left(self):
        return self.corner.x
    
    def right(self):
        return self.corner.x + self.width
    
    def bottom(self):
        return self.corner.y
    
    def top(self):
        return self.corner.y + self.height
    
    def corners(self):
        c1 = Point(self.left(), self.bottom())
        c2 = Point(self.left(), self.top())
        c3 = Point(self.right(), self.bottom())
        c4 = Point(self.right(), self.top())
        return [c1, c2, c3, c4]
        
    def covers(self, obj):
        if isinstance(obj, Point):
            return self.left() <= obj.x <= self.right() and self.bottom() <= obj.y <= self.top()
        if isinstance(obj, Rectangle):
            oc = obj.corners()
            sc = self.corners()
            return self.covers(oc[0]) or self.covers(oc[1]) or self.covers(oc[2]) or self.covers(oc[3]) or obj.covers(sc[0]) or obj.covers(sc[1]) or obj.covers(sc[2]) or obj.covers(sc[3])
        return False
        
    def intersect(self, obj):
        if isinstance(obj, Point):
            if self.covers(obj):
                return obj
        if isinstance(obj, Rectangle):
            if self.covers(obj):
                left = max(self.left(), obj.left())
                right = min(self.right(), obj.right())
                bottom = max(self.bottom(), obj.bottom())
                top = min(self.top(), obj.top())
                return Rectangle(Point(left, bottom), right-left, top-bottom)
        return None

    def plot(self, name=None):
        x = []
        y = []
        x.append(self.left())
        y.append(self.bottom())
        x.append(self.left())
        y.append(self.top())
        x.append(self.right())
        y.append(self.top())
        x.append(self.right())
        y.append(self.bottom())
        x.append(self.left())
        y.append(self.bottom())
        
        plot(x, y)
        if name:
            text((self.right()+self.left())/2,
                 (self.top()+self.bottom())/2, name)
        else:
            text((self.right()+self.left())/2,
                 (self.top()+self.bottom())/2, self.__str__())

