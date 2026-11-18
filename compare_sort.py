
import time

from main import sort_on_median, read_keys


def library_sort(keys):
    return sorted(keys, key=lambda x: x[0])



def same_values(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i][0] != b[i][0]:   
            return False
    return True


def main():
    n = 249480
    keys = read_keys("17-Семин_К/keys.txt")

    t0 = time.perf_counter()
    my_res = sort_on_median(list(keys))
    my_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    lib_res = library_sort(list(keys))
    lib_time = time.perf_counter() - t0

    print(f"n = {n}")
    print(f"моя сортировка: {my_time:.4f} c")
    print(f"библиотечная:   {lib_time:.4f} c")
    if lib_time > 0:
        print(f"моя медленнее в {my_time / lib_time:.2f} раз")
    if my_res != lib_res:
        print("ОШИБКА: результаты не совпадают (в т.ч. возможна потеря устойчивости)")
    

if __name__ == "__main__":
    main()