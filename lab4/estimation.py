from ec import *
import time

if __name__ == '__main__':
    p = 50000017
    E = get_random_curve(p)
    x, y  = get_random_xy(E)
    P = Point(x, y, E)
    time_sum=0
    R = Point.infinity(P.curve)
    n = 1
    while True:
        start = time.perf_counter()
        R = add(R, P)
        if R.is_infinity():
            break
        n += 1
        elapsed = time.perf_counter() - start
        time_sum+=elapsed
    print(f"p={p}, a={E.a}, b={E.b}, P=({x},{y}), order={n}, time={time_sum:.2f}s")
    print(f"Avg iter time = {time_sum / (n-1)}")

