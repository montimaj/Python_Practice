import provided.class_exercise_geometry as geometry

def intersects(rectangles, r):
    i=0
    while i<len(rectangles):
        if i!=r and rectangles[3].intersect(rectangles[i]):
            return True
        i+=1
    return False

def dist_points(points):
    distance_dict={}
    for point1 in points:
        for point2 in points:
            if point1!=point2:
                distance_dict[(point1,point2)]=point1.distance(point2)
    return distance_dict

def closest_points(distance_dict, point):
    new_dict={}
    for points, dist in distance_dict.items():
        if points[0]==point:
            new_dict[points[1]]=dist
    min_dist=[]
    min_val=min(new_dict.values())
    for k,v in new_dict.items():
        if v==min_val:
            min_dist.append((k,v))
    return min_dist

def minimum_dist(distance_dict):
    min_dist=min(distance_dict.values())
    minimum=[]
    flag={}
    for k,v in distance_dict.items():
        if (k[0],k[1]) not in flag.keys() and (k[1],k[0]) not in flag.keys() and v==min_dist:
            flag[k]=True
            minimum.append(((k[0].x,k[0].y),(k[1].x, k[1].y),v))
    return minimum

def to_values(points):
    text=''
    for point in points:
        text+='('+str(point[0].x)+','+str(point[0].y)+'): '+str(point[1])+'\n'
    return text

points=((1,8),(4,4),(6,6),(6,1),(8,8),(8,3))
rectangle=(((2,1),3,8),((3,2),6,3),((3,3),4,4),((8,7),2,2))
point_obj=[]
rectangles=[]
for point in points:
    point_obj.append(geometry.Point(point[0], point[1]))
for data in rectangle:
    r=geometry.Rectangle(geometry.Point(data[0][0], data[0][1]), data[1], data[2])
    print(r)
    rectangles.append(r)


print('Distance between p1 and p2:', point_obj[0].distance(point_obj[1]))
print('p1 covered by r1:',rectangles[0].covers(point_obj[0]))
print('p1 covered by r2:',rectangles[1].covers(point_obj[0]))
print('p1 covered by r3:',rectangles[1].covers(point_obj[0]))
print('p1 covered by r4:',rectangles[1].covers(point_obj[0]))
print('r4 intersects with any other rectangles?:',intersects(rectangles, 3))
print('Intersection of r1 and r4:', rectangles[0].intersect(rectangles[3]))
print('r2 covered by r1:',rectangles[0].covers(rectangles[1]))
print('Intersection of r1,r2,r3:', rectangles[2].intersect(rectangles[1].intersect(rectangles[0])))
dist_dict=dist_points(point_obj)
print('Points closest to p1:', to_values(closest_points(dist_dict, point_obj[0])))
print('Minimum distance between all points:', minimum_dist(dist_dict))

'''
Distance between p1 and p2: 5.0
p1 covered by r1: False
p1 covered by r2: False
p1 covered by r3: False
p1 covered by r4: False
r4 intersects with any other rectangles?: False
Intersection of r1 and r4: None
r2 covered by r1: True
Intersection of r1,r2,r3: Rectangle(Point(3, 3), 2, 2)
Points closest to p1: (4,4): 5.0
Minimum distance between all points: 2.8284271247461903
'''
