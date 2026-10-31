import time
from typing import Callable
import gc


def slow_func(arr: list[int]) -> bool: #Time Comp -> O(N^2), Space Comp -> O(1)
    n = len(arr) 
    for i in range(n):
        for j in range(i+1,n):
            if arr[i]== arr[j]:
                return True
    return False


def fast_func(arr: list[int]) -> bool: #Time Comp-> O(N), Space Comp -> O(N)
    seen = set()
    for i in arr:
        if i in seen:
            return True
        seen.add(i) 
    return False


def bin_search_func(arr: list[int]) -> bool: # Time Comp -> O(log N), Space Comp -> O(1)
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == -1:
            return True

        elif arr[mid] < -1:
            left = mid + 1
        else:
            right = mid - 1

    return False


def measure_time(func: Callable, data: list[int], repeats: int = 5) -> float: #timer 
    func(data)
    measurements = []
    for _ in range(repeats):
        gc.disable()
        start = time.perf_counter()
    
        func(data)

        finish = time.perf_counter()
        gc.enable()
    
        measurements.append((finish-start)*1000) #ms
    return min(measurements)


def run_bench(func_name: str,func: Callable, sizes:list[int]):
    print(f"Function {func_name} started.\n")
    prev_time = None
    ratios = []
    
    for size in sizes:
        data = list(range(size)) # Worst-case scenario: unique elements force complete traversal
        current_time = measure_time(func,data)

        if prev_time is None:
            print(f"N = {size}, Time: {current_time:.3f} ms | Baseline\n")
        else:
            ratio = current_time / prev_time
            ratios.append(ratio)
            print(f"N = {size}, Time: {current_time:.3f} ms | Ratio: {ratio:.2f}x")
        prev_time = current_time

    avg_ratio = sum(ratios) / len(ratios) if ratios else 1.0

    # Estimate empirical Big-O complexity based on the average growth ratio
    if avg_ratio < 1.5:
        complexity = "O(1) or O(log N)"
    elif avg_ratio < 3.0:
        complexity = "O(N) or O(N log N)"
    elif avg_ratio < 6.0:
        complexity = "O(N^2)"
    else:
        complexity = "O(N^3) or higher"

    print(f"\n>> Estimated Complexity: {complexity} (Avg Ratio: {avg_ratio:.2f}x)\n")



    
if __name__ == "__main__":
    sizes = [1000,2000,4000,8000,16000,32000]
    run_bench("fast_func",fast_func, sizes)
    run_bench("slow_func",slow_func, sizes)
    run_bench("bin_search_func", bin_search_func, sizes)
