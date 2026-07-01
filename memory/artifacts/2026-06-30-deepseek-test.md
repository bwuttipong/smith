# DeepSeek V4 Flash Test - Binary Search

```python
from typing import List

def binary_search(arr: List[int], target: int) -> int:
    """
    Perform binary search on a sorted list of integers.
    
    Args:
        arr: Sorted list of integers (ascending order)
        target: Integer to search for
    
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Test cases
if __name__ == "__main__":
    test_arr = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"Array: {test_arr}")
    print(f"Search 7: {binary_search(test_arr, 7)}")    # 3
    print(f"Search 1: {binary_search(test_arr, 1)}")    # 0
    print(f"Search 15: {binary_search(test_arr, 15)}")  # 7
    print(f"Search 8: {binary_search(test_arr, 8)}")    # -1
    print(f"Search 0: {binary_search(test_arr, 0)}")    # -1
    print(f"Empty array: {binary_search([], 5)}")       # -1
```
