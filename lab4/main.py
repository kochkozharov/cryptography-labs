from ec import *


def find_curve(p, min_seconds=540, max_seconds=660):
    while True:
        E = get_random_curve(p)
        x, y = get_random_xy(E)
        P = Point(x, y, E)
        order, elapsed = brute_order(P, max_seconds)
        print(f"p={p}, a={E.a}, b={E.b}, P=({x},{y}), order={order}, time={elapsed:.2f}s")
        if order is None:
            print(f"Timeout after {max_seconds}s")
            continue
        if elapsed < min_seconds:
            print(f"Too fast: only {elapsed:.2f}s")
            continue
        return E, P, order, elapsed

if __name__ == '__main__':
    p = 387272759
    curve, point, order, elapsed = find_curve(p)
    print("\nSelected curve and point:")
    print(f"y^2 = x^3 + {curve.a}x + {curve.b} (mod {curve.p})")
    print(f"Point P = ({point.x}, {point.y}), order = {order}, computed in {elapsed:.2f}s")
