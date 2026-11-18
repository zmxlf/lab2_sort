import argparse
import sys
import time
import statistics




def sort_on_median(keys):

    if len(keys)<=1:
        return keys
    
    first = keys[0][0]
    last = keys[-1][0]
    midle = keys[len(keys)//2][0]

    if (first<=midle<=last) or (last<=midle<=first):
        median = midle
    elif (midle<=first<=last) or (last<=first<=midle):
        median = first
    else:
        median = last

    left = [x for x in keys if x[0]<median]
    sred = [x for x in keys if x[0]==median]
    right = [x for x in keys if x[0]>median]

    return sort_on_median(left) + sred + sort_on_median(right)


def read_keys(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    n = int(lines[0])
    keys =[]
    
    for i in range(n):
        
        keys.append((int(lines[i+1]),i))
    
    
    return keys
    


def read_bmp(path):
    with open(path, "rb") as f:
        data = f.read()

        if len(data) < 54:
            raise ValueError( "файл меншье 54 байт")
        if data[0:2]!= b"BM":
            raise ValueError( "неыерная сигнатура")

        bfOffBits= int.from_bytes(data[10:14],"little")
        biSize= int.from_bytes(data[14:18],"little")
        biWidth= int.from_bytes(data[18:22],"little")
        biHeight = int.from_bytes(data[22:26],"little",signed=True)
        biBitCount = int.from_bytes(data[28:30],"little")
        biCompression= int.from_bytes(data[30:34],"little")

        if biBitCount != 24:
            raise ValueError( f"ожидался 24-бит BMP, получено {biBitCount}")
        if biCompression != 0:
            raise ValueError( f"сжатие не поддерживается (biCompression={biCompression})")
        if biWidth <= 0 or biHeight == 0:
            raise ValueError( f"некорректные размеры: {biWidth}x{biHeight}")
        if bfOffBits > len(data):
            raise ValueError( "bfOffBits за пределами файла")

        w = biWidth
        h = abs(biHeight)
        size = (w*3+3)//4*4

        pixels = bytearray((w*3)*h)
        pos = bfOffBits
        dist = 0

        for i in range(h):
            pixels[dist:dist+(w*3)] = data[pos:pos + (w*3)]
            dist+=w*3
            pos+=size

        return {
            "raw":      bytearray(data),   
            "width":    w,
            "height":   h,
            "start":   bfOffBits,
            "row_size": size,
            "pixels":   pixels,          
            "n":        w * h,   
        }


def sort_bmp(pixels,sorted_kyes):

    n = len(sorted_kyes)
    new_pixels = bytearray(n*3)

    for i in range(n):
        old_id = sorted_kyes[i][1]

        s= old_id*3
        dst = i*3

        new_pixels[dst] = pixels[s]
        new_pixels[dst+1] = pixels[s+1]
        new_pixels[dst+2] = pixels[s+2]

    return new_pixels

def write_bmp(path,bmp,new_pixels):
    data = bytearray(bmp["raw"])
    w = bmp["width"]
    h = bmp["height"]
    pos = bmp["start"]

    dist = 0
    row_str= w*3

    for i in range(h):
        data[pos: pos+row_str] = new_pixels[dist:dist+row_str]

        dist+=row_str
        pos+=bmp["row_size"]

    with open(path,"wb") as f:
        f.write(data)


def main():
    # bmp_path = "17-Семин_К/shuffled.bmp"
    # keys_path = "17-Семин_К/keys.txt"
    # newbmp_path = "17-Семин_К/restored.bmp"


    # try:
    #     bmp = read_bmp(bmp_path)
    #     keys = read_keys(keys_path)

    #     if len(keys) != bmp["n"]:
    #         raise ValueError(f"Ключей {len(keys)} не совпадает с пикселями {bmp['n']}")

    #     sorted_keys = sort_on_median(keys)
    #     new_pixels= sort_bmp(bmp["pixels"],sorted_keys)
    #     write = write_bmp(newbmp_path,bmp,new_pixels)
    # except Exception as e:
    #     print(f"ошибка {e}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--bmp", required=True)
    parser.add_argument("--keys", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--bench", type=int, default=0)  # пока не используется
    args = parser.parse_args()
 
    bmp_path = args.bmp
    keys_path = args.keys
    newbmp_path = args.out
    
    try:
        bmp = read_bmp(bmp_path)
        keys = read_keys(keys_path)
 
        if len(keys) != bmp["n"]:
            raise ValueError(f"Ключей {len(keys)} не совпадает с пикселями {bmp['n']}")

        
        # --- БЛОК БЕНЧМАРКА ---
        if args.bench > 0:
            times = []
            for _ in range(args.bench):
                t0 = time.perf_counter()
                sorted_keys = sort_on_median(keys)
                t1 = time.perf_counter()
                times.append((t1 - t0) * 1000)

            median_time = statistics.median(times)
            min_time = min(times)
            max_time = max(times)
            checksum = sum(k[0] for k in keys)

            
            print(f"Медиана сортировки: {median_time:.3f} мс")
            print(f"Мин: {min_time:.3f} мс, Макс: {max_time:.3f} мс")
            print(f"Контрольная сумма (сумма ключей): {checksum}")
        else:
            
            sorted_keys = sort_on_median(keys)
        
        new_pixels= sort_bmp(bmp["pixels"],sorted_keys)
        write_bmp(newbmp_path,bmp,new_pixels)


    except Exception as e:
        print(f"ошибка {e}")
        sys.exit(1)


if __name__=="__main__":
   
    main()
