import time
from typing import Callable


def slow_fonk(arr: list[int]) -> bool: #Time Comp -> O(N^2), Space Comp -> O(1)
    n = len(arr) 
    for i in range(n):
        for j in range(i+1,n):
            if arr[i]== arr[j]:
                return True
    return False

def fast_fonk(arr: list[int]) -> bool: #Time Comp-> O(N), Space Comp -> O(N)
    seen = set()
    for i in arr:
        if i in seen:
            return True
        seen.add(i) 
    return False


def measure_time(func: Callable, data: list[int]) -> float: #timer
    start = time.perf_counter()
    
    func(data)

    finish = time.perf_counter()

    return (finish-start)*1000 #ms

def run_bench(func_name: str,func: Callable, sizes:list[int]):
    print(f"Function {func_name} started.\n")
    prev_time = None
    last_ratio = 1.0

    for size in sizes:
        data = list(range(size)) # Worst-case scenario: unique elements force complete traversal
        current_time = measure_time(func,data)

        if prev_time is None:
            print(f"N = {size}, Time: {current_time:.3f} ms | Baseline\n")
        else:
            ratio = current_time / prev_time
            last_ratio = ratio
            print(f"N = {size}, Time: {current_time:.3f} ms | Ratio: {ratio:.2f}x")
        prev_time = current_time

    # Estimate empirical Big-O complexity based on the final growth ratio
    if last_ratio < 1.3: 
        complexity = "O(1) or O(log N)"
    elif 1.3 <= last_ratio < 2.7:
        complexity = "O(N) or O(N log N)"
    else:
        complexity = "O(N^2)"

    print(f"\n>> Estimated Complexity: {complexity}\n")



    
if __name__ == "__main__":
    sizes = [1000,2000,4000,8000,10000]
    run_bench("fast_fonk",fast_fonk, sizes)
    run_bench("slow_fonk",slow_fonk, sizes)
