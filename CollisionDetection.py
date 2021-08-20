import numpy as np

dimension = 2

# 判斷是否跟方向D同方向(+-90度)
def SameDirection(direction, ao):
    return np.dot(direction, ao) > 0

class Collider:
    def __init__(self, vertices):
        self.vertices = vertices
    # 找到跟方向D內積最大的頂點
    def FindFurthestPoint(self, direction):
        maxDistance = np.finfo(float).min
        for vertex in self.vertices:
            distance = np.dot(vertex, direction)
            if(distance > maxDistance):
                maxDistance = distance
                maxPoint = vertex
        return maxPoint

# 兩個形狀找出的頂點所形成的向量(這些向量末點可以構成圖形，如果圖形包含原點在內則代表碰撞)
def Support(colliderA, colliderB, direction):
    return np.subtract(colliderA.FindFurthestPoint(direction), colliderB.FindFurthestPoint(np.multiply(direction, -1)))

class Simplex:
    def __init__(self):
        self.points = (0,0,0,0)
        self.size = 0
        self.direction = (1, 0, 0)
    def push_front(self, point):
        self.points = (point, self.points[0], self.points[1], self.points[2])
        self.size = min(self.size + 1, 4)
def GJK(colliderA, colliderB):
    points = Simplex()
    support = Support(colliderA, colliderB, points.direction)
    points.push_front(support)
    points.direction = np.multiply(support, -1)
    while(True):
        support = Support(colliderA, colliderB, points.direction)
        if(np.dot(support, points.direction) <= 0):
            return False
        points.push_front(support)
        if(NextSimplex(points, points.direction)):
            return True

def NextSimplex(points, direction):
    x = points.size
    if(x == 2):
        return Line(points, direction)
    elif(x == 3):
        return Triangle(points, direction)
    elif(x == 4):
        return Tetrahedron(points, direction)
    return False

def Line(points, direction):
    a = points.points[0]
    b = points.points[1]
    ab = np.subtract(b, a)
    ao = np.multiply(a, -1)
    if(SameDirection(ab, ao)):
        direction = np.cross(ab, ao)
        points.direction = np.cross(direction, ab)
    else:
        points.points = (a,0,0,0)
        points.size = 1
        points.direction = ao
    return False

def Triangle(points, direction):
    a = points.points[0]
    b = points.points[1]
    c = points.points[2]
    ab = np.subtract(b, a)
    ac = np.subtract(c, a)
    ao = np.multiply(a, -1)
    abc = np.cross(ab, ac)
    if(SameDirection(np.cross(abc, ac), ao)):
        if(SameDirection(ac, ao)):
            points.points = (a, c, 0, 0)
            points.size = 2
            direction = np.cross(ac, ao)
            points.direction = np.cross(direction, ac)
        else:
            points.points = (a, b, 0, 0)
            return Line(points, direction)
    else:
        if(SameDirection(np.cross(ab, abc), ao)):
            points.points = (a, b, 0, 0)
            return Line(points, direction)
        else:
            if(SameDirection(abc, ao)):
                points.direction = abc
            else:
                points.points = (a, c, b, 0)
                points.direction = np.multiply(abc, -1)
    if(dimension == 2):
        return True
    if(dimension == 3):
        return False

def Tetrahedron(points, direction):
    a = points.points[0]
    b = points.points[1]
    c = points.points[2]
    d = points.points[3]
    ab = np.subtract(b, a)
    ac = np.subtract(c, a)
    ad = np.subtract(d, a)
    ao = np.multiply(a, -1)
    abc = np.cross(ab, ac)
    acd = np.cross(ac, ad)
    adb = np.cross(ad, ab)
    if(SameDirection(abc, ao)):
        return Triangle((a, b, c, 0), direction)
    if(SameDirection(acd, ao)):
        return Triangle((a, c, d, 0), direction)
    if(SameDirection(adb, ao)):
        return Triangle((a, d, b, 0), direction)
    return True
