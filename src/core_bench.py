import time

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


def mesaure_time(func, data: list[int]) -> float: #timer
    start = time.perf_counter()
    
    func(data)

    finish = time.perf_counter()

    return (finish-start)*1000 #ms
