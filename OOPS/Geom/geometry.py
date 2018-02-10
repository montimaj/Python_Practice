class Point:
    __x=0.
    __y=0.
    def __init__(self, x=0., y=0.):
        try:
            if isinstance(x,(int,float)) and isinstance(y,(int,float)):
                self.__x=x
                self.__y=y
            else:
                raise ValueError("Invalid input for point")
        except ValueError as err:
                print(err)

    def getxy(self):
        return self.__x, self.__y

    def get_distance(self, other):
        return ((self.__x-other.__x)**2 + (self.__y-other.__y)**2)**0.5

    def on_segment(self, line_segment):
        p,r=line_segment.get_points()
        px,py=p.getxy()
        rx,ry=r.getxy()
        qx,qy=self.getxy()
        epsilon=1E-8
        return qx>=min(px,rx)-epsilon and qx<=max(px,rx)+epsilon and qy>=min(py,ry)-epsilon and qy<=max(py,ry)+epsilon

class LineSegment:
    __p1=Point()
    __p2=Point()

    def __init__(self, p1=Point(), p2=Point()):
        try:
            if isinstance(p1, Point) and isinstance(p2, Point):
                self.__p1=p1
                self.__p2=p2
            else:
                raise ValueError("Invalid input for line segment")
        except ValueError as err:
            print(err)

    def get_points(self):
        return self.__p1, self.__p2

    def get_knowns(self):
        a,b=self.get_points()
        ax,ay=a.getxy()
        bx,by=b.getxy()
        a1=by-ay
        b1=ax-bx
        c1=a1*ax + b1*ay
        return a1, b1, c1

    def get_length(self):
        a,b=self.get_points()
        ax,ay=a.getxy()
        bx,by=b.getxy()
        return ((ax-bx)**2 + (ay-by)**2)**0.5

    def intersection(self,other):
        #Line AB a1x + b1y = c1
        a1, b1, c1 = self.get_knowns()

        #Line CD a2x + b2y = c2
        a2, b2, c2 = other.get_knowns()

        det=a1*b2-a2*b1
        if det:
            x=(b2*c1-b1*c2)/det
            y=(a1*c2-a2*c1)/det
            p=Point(x,y)
            if p.on_segment(other) and p.on_segment(self):
                return True, p.getxy()
        return False

class LineString():
    __line_string=[]

    def __init__(self, list_ls):
        self.__line_string=list_ls

    def set_of_points(self):
        points=set()
        for ls in self.__line_string:
            for point in ls.get_points():
                points.add(point.getxy())
        return points

    def self_intersects(self):
        for ls1 in self.__line_string:
            for ls2 in self.__line_string:
                in_point=ls1.intersection(ls2)
                if in_point and ls1!=ls2 and in_point[1] not in self.set_of_points():
                       return in_point
        return False

    def is_closed(self):
        start_point=self.__line_string[0].get_points()[0]
        end_point=self.__line_string[-1].get_points()[1]
        return start_point.getxy()==end_point.getxy()

class Polygon:
    __poly=[]

    def __init__(self, poly):
        self.__poly=poly

    def set_of_points(self):
        points=set()
        for ls in self.__poly:
            for point in ls.get_points():
                points.add(point.getxy())
        return points

    def num_cuts(self, line_segment):
        numcuts=0
        cut_points={}
        for ls in self.__poly:
            in_point=ls.intersection(line_segment)
            if in_point and in_point[1] not in cut_points.keys() and in_point[1]!=line_segment.get_points()[1].getxy():
                print('Cut #'+str(numcuts+1)+': ', in_point[1])
                cut_points[in_point[1]]=True
                numcuts+=1
        return numcuts

    def is_inside(self, geom, entirely_inside=False):
        if geom in self.set_of_points():
            if entirely_inside:
                return False
            return True
        if entirely_inside:
            for ls in self.__poly:
                if geom.on_segment(ls):
                    return False
        max_x=max(self.set_of_points())[0]
        ls=LineSegment(geom, Point(float(max_x),float(geom.getxy()[1])))
        return self.num_cuts(ls)%2!=0

    def is_containing(self, other, entirely=False):
        points=other.set_of_points()
        for point in points:
            if not self.is_inside(Point(point[0], point[1]), entirely):
                return False
        print('All points inside')
        for ls1 in other.__poly:
            for ls2 in self.__poly:
                if ls1.intersection(ls2):
                    return False
        return True

class Inputs:
    @staticmethod
    def input_line_segments():
        try:
            n=int(input('Number of line segments?: '))
            if n<1:
                raise ValueError('Must be positive')
            else:
                line_segments=[]
                for i in range(n):
                    print('Line #'+str(i+1)+':')
                    try:
                        x=float(input('Enter x1: '))
                        y=float(input('Enter y1: '))
                        p1=Point(x,y)
                        x=float(input('Enter x2: '))
                        y=float(input('Enter y2: '))
                        p2=Point(x,y)
                        ls=LineSegment(p1,p2)
                        print('Length: ',ls.get_length(),'\n')
                        line_segments.append(ls)
                    except ValueError:
                        print("Invalid input")
                return line_segments
        except ValueError as err:
            print(err)

ls_list=[1]#Inputs.input_line_segments()
if ls_list:
    '''
    Successful tests
    #line_string=LineString(ls_list)
    #print('Intersecting?: ', ls_list[0].intersection(ls_list[1]))
    #print('Self Intersecting?: ', line_string.self_intersects())
    #print('Is closed?: ', line_string.is_closed())
    #poly=Polygon(ls_list)
    #poly=Polygon([LineSegment(Point(5,0), Point(3,2)), LineSegment(Point(3,2),Point(1,3)), LineSegment(Point(1,3),Point(2,4)), LineSegment(Point(2,4),Point(5,1)), LineSegment(Point(5,1),Point(7,2)), LineSegment(Point(7,2),Point(5,0))])
    #poly=Polygon([LineSegment(Point(6.48,-1.6), Point(4.08,3.62)), LineSegment(Point(4.08,3.62),Point(1,3)), LineSegment(Point(1,3),Point(6.83,5.98)), LineSegment(Point(6.83,5.98),Point(5.18,1.9)), LineSegment(Point(5.18,1.9),Point(8.35,4.98)), LineSegment(Point(8.35,4.98),Point(6.48,-1.6))])
    #poly=Polygon([LineSegment(Point(8.43,1.77), Point(-1.86,-2.28)), LineSegment(Point(-1.86,-2.28),Point(4.08,3.62)), LineSegment(Point(4.08,3.62),Point(-0.86,11.41)), LineSegment(Point(-0.86,11.41),Point(6.83,5.98)), LineSegment(Point(6.83,5.98),Point(14,10)), LineSegment(Point(14,10),Point(8.43,1.77))])
    #test_ls=LineSegment(Point(1,2),Point(8,1))
    #print('Num_cuts: ', poly.num_cuts(test_ls))
    #print('Point inside polygon?: ', poly.is_inside(Point(3.56,2.01)))
    #test_poly=Polygon([LineSegment(Point(3.56, 2.01), Point(7.75,4.46)),LineSegment(Point(7.75, 4.46), Point(3.57,6.73)), LineSegment(Point(3.57,6.73), Point(3.56,2.01))])
    #test_poly=Polygon([LineSegment(Point(4.1, 2.01), Point(8.42,5.6)),LineSegment(Point(8.42, 5.6), Point(4.1,6.73)), LineSegment(Point(4.1,6.73), Point(4.1,2.01))])
    #test_poly=Polygon([LineSegment(Point(4.1, 2.01), Point(8.39,5.54)),LineSegment(Point(8.39, 5.54), Point(4.08,6.68)), LineSegment(Point(4.08,6.68), Point(4.1,2.01))])
    #test_poly=Polygon([LineSegment(Point(4, 2), Point(5,5.11)),LineSegment(Point(5, 5.11), Point(8.3,5.53)), LineSegment(Point(8.3,5.53), Point(8,2)), LineSegment(Point(8,2), Point(4,2))])
    #test_poly=Polygon([LineSegment(Point(2.68, -0.96), Point(5,5.11)),LineSegment(Point(5, 5.11), Point(8.3,5.53)), LineSegment(Point(8.3,5.53), Point(8,2)), LineSegment(Point(8,2), Point(2.68,-0.96))])
    #test_poly=Polygon([LineSegment(Point(4.08, 3.62), Point(5,5.11)),LineSegment(Point(5, 5.11), Point(8.3,5.53)), LineSegment(Point(8.3,5.53), Point(8,2)), LineSegment(Point(8,2), Point(4.08,3.62))])
    #print('Poly inside poly?: ', poly.is_containing(test_poly))
    '''