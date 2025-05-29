import numpy as np

def bubble_sort(arr):
    arr = arr.copy()  # vermeidet In-Place-Änderung
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
        
if __name__ == "__main__": 
    test_array = np.array([5, 2, 9, 1, 5, 6])
    print(bubble_sort(test_array))