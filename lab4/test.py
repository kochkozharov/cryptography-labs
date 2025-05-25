from ec import *

if __name__ == '__main__':
    p = 426000017
    a = 131325779
    b = 8713283
    E = EllipticCurve(a, b, p)
    point = (12195349,21713483)
    x, y  = point
    P = Point(x, y, E)
    order, elapsed = brute_order(P)
    print(f"p={p}, a={E.a}, b={E.b}, P=({x},{y}), order={order}, time={elapsed:.2f}s")
