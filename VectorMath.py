import math

def Distance(ax = 0.0, ay = 0.0, bx = 0.0, by = 0.0):
    x = ax - bx;
    x *= x;
    y = ay - by;
    y*= y;
    return (math.sqrt(x + y));

def DistanceNormalized(ax = 0.0, ay = 0.0, bx = 0.0, by = 0.0, size = 256):
    dist = Distance(ax, ay, bx, by);
    dist /= size;
    return dist;