import random
import signal
import time


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


def get_random_xy(E):
    while True:
        x = random.randrange(E.p)
        rhs = (x**3 + E.a*x + E.b) % E.p
        y = None
        for yy in range(E.p):
            if yy*yy % E.p == rhs:
                y = yy
                break
        if y:
            break
        else:
            continue
    return x, y

def get_random_curve(p):
    while True:
        a = random.randrange(p)
        b = random.randrange(p)
        try:
            E = EllipticCurve(a, b, p)
            break
        except ValueError:
            continue
    return E

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