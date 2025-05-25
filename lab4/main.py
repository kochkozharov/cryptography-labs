import random
import time
import signal

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("Singular curve")

class Point:
    def __init__(self, x=None, y=None, curve=None):
        self.x = x
        self.y = y
        self.curve = curve

    def is_infinity(self):
        return self.x is None and self.y is None

    @staticmethod
    def infinity(curve):
        return Point(None, None, curve)

def add(P, Q):
    curve = P.curve
    p = curve.p
    if P.is_infinity(): return Q
    if Q.is_infinity(): return P
    if P.x == Q.x and (P.y + Q.y) % p == 0:
        return Point.infinity(curve)
    if P.x == Q.x:
        lam = (3 * P.x * P.x + curve.a) * pow(2 * P.y, -1, p) % p
    else:
        lam = ((Q.y - P.y) * pow(Q.x - P.x, -1, p)) % p
    x_r = (lam * lam - P.x - Q.x) % p
    y_r = (lam * (P.x - x_r) - P.y) % p
    return Point(x_r, y_r, curve)

def mul(P, n):
    R = Point.infinity(P.curve)
    Q = P
    while n > 0:
        if n & 1:
            R = add(R, Q)
        Q = add(Q, Q)
        n >>= 1
    return R

class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError

def brute_order(P, max_seconds=660):
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(max_seconds)
    start = time.perf_counter()
    try:
        R = Point.infinity(P.curve)
        n = 1
        while True:
            R = add(R, P)
            if R.is_infinity():
                break
            n += 1
        elapsed = time.perf_counter() - start
        signal.alarm(0)
        return n, elapsed
    except TimeoutError:
        elapsed = time.perf_counter() - start
        signal.alarm(0)
        return None, elapsed

def find_curve(p, min_seconds=540, max_seconds=660):
    while True:
        a = random.randrange(p)
        b = random.randrange(p)
        try:
            E = EllipticCurve(a, b, p)
        except ValueError:
            continue
        x = random.randrange(p)
        rhs = (x**3 + a*x + b) % p
        y = None
        for yy in range(p):
            if yy*yy % p == rhs:
                y = yy
                break
        if y is None:
            continue
        P = Point(x, y, E)
        order, elapsed = brute_order(P, max_seconds)
        print(f"p={p}, a={a}, b={b}, P=({x},{y}), order={order}, time={elapsed:.2f}s")
        if order is None:
            print(f"Timeout after {max_seconds}s")
            continue
        if elapsed < min_seconds:
            print(f"Too fast: only {elapsed:.2f}s")
            continue
        return E, P, order, elapsed

if __name__ == '__main__':
    p = 426000017
    curve, point, order, elapsed = find_curve(p)
    print("\nSelected curve and point:")
    print(f"y^2 = x^3 + {curve.a}x + {curve.b} (mod {curve.p})")
    print(f"Point P = ({point.x}, {point.y}), order = {order}, computed in {elapsed:.2f}s")
