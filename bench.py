import random
import statistics
import time

from main import sort_on_median


def make_keys(n, seed=42):
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


def measure(func, keys, repeats):
    
    func(list(keys))

    times = []
    for _ in range(repeats):
        times.append(time_one(func, list(keys)))   # каждый раз свежая копия

    return statistics.median(times), min(times), max(times)


def main():
    sizes = [40000, 55696, 78400, 160000, 249480, 313600, 701406]
    repeats = 7

    print(f"{'n':>7} | {'моя, c':>8} | {'мин':>8} | {'макс':>8} | {'разброс %':>9} | {'sorted, c':>9} | {'во сколько раз':>14}")
    print("-" * 82)

    for n in sizes:
        keys = make_keys(n)

        my_med, my_min, my_max = measure(sort_on_median, keys, repeats)
        lib_med, lib_min, lib_max = measure(lambda k: sorted(k, key=lambda x: x[0]), keys, repeats)

        spread = (my_max - my_min) / my_med * 100
        ratio = my_med / lib_med

        print(f"{n:>7} | {my_med:>8.4f} | {my_min:>8.4f} | {my_max:>8.4f} | {spread:>9.1f} | {lib_med:>9.4f} | {ratio:>14.2f}")


if __name__ == "__main__":
    main()