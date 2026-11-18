

import random
import time

from main import sort_on_median


def make_keys(n, seed=1):
    random.seed(seed)
    keys = []
    for i in range(n):
        keys.append((random.randint(0, 1_000_000), i))
    return keys


def time_one(func, keys):
    t0 = time.perf_counter()
    func(keys)
    t1 = time.perf_counter()
    return t1 - t0


def main():
    sizes = [ 40000, 55696, 78400,160000,313600,701406]
    repeats = 3  

    print(f"{'n':>7} | {'моя, c':>10} | {'sorted, c':>10}")
    print("-" * 31)



    for n in sizes:
        my_best = None
        lib_best = None

        for _ in range(repeats):
            keys = make_keys(n)

            t = time_one(sort_on_median, list(keys))
            if my_best is None or t < my_best:
                my_best = t

            t = time_one(lambda k: sorted(k, key=lambda x: x[0]), list(keys))
            if lib_best is None or t < lib_best:
                lib_best = t

        

        print(f"{n:>7} | {my_best:>10.4f} | {lib_best:>10.4f}")



if __name__ == "__main__":
    main()