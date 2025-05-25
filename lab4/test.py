from ec import *

if __name__ == '__main__':
    p = 387272759
    a = 124860295
    b = 2186117
    E = EllipticCurve(a, b, p)
    point = (223741075,161701677)
    x, y  = point
    P = Point(x, y, E)
    order, elapsed = brute_order(P)
    print(f"p={p}, a={E.a}, b={E.b}, P=({x},{y}), order={order}, time={elapsed:.2f}s")
