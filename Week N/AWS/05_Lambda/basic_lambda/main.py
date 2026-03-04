from typing import Optional


def binary_search(arr: list, target: int) -> Optional[int]:
    start, end = 0, len(arr) - 1

    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            end = mid - 1
        else:
            end = mid + 1

    return -1


if __name__ == "__main__":
    my_array = [1, 3, 5, 6, 8, 9, 32, 21]
    print(
        f"Number 3 can be found at index {binary_search(arr=my_array, target=3)} in this {my_array} array"
    )
