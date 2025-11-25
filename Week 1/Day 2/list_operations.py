from typing import Any


def append_element(arr: list[Any], item: Any):
    """
    Add an item at the end of an array
    Args:
        arr: list for appending
        item: item to append
    """
    arr.append(item)

def slice_list(arr: list[Any], start: int, end: int) -> list[Any]:
    """
    Slice a list from a start to end index
    Args:
        arr: list to slice
        start: start index (inclusive)
        end: end index (exclusive)
    """
    return arr[start: end]

def insert_element(arr: list[Any], element: Any, i: int) -> None:
    """
    insert an element at given index
    Args:
        arr: list to insert
        element: element to be inserted
        i: index to insert the element
    """
    arr.insert(i, element)

def reverse_list(arr: list[Any]) -> list[Any]:
    """
    Reverse all the elements in a list in-place
    Args:
        arr: list to reverse
    Returns:
        the same list (arr)
    """
    l, r = 0, len(arr) - 1  # noqa: E741
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1  # noqa: E741
        r -= 1

    return arr

def pop_element(arr: list[Any], index: int | None) -> Any:
    """
    Remove element from a list if there is index else from last and
    returns the popped element
    Args:
        arr: list to pop from
        index: position of the element in the list
    Returns:
        returns the popped element
    """
    if index:
        return pop_element_at(index=index, arr=arr)
    return arr.pop()

def pop_element_at(index: int, arr: list[Any]) -> Any:
    """
    Remove element from a list at given index
    Args:
        index: index to remove at
        arr: list to remove from
    Returns:
        Returns the popped element
    """
    return arr.pop(index)

def count_element(arr: list[Any], element: Any) -> int:
    """
    Count the occurance of a particular element in a list
    Args:
        arr: list to look for the element
        element: element's occurance to count
    Returns:
        the count of occurance of the element
    """
    count = 0
    for item in arr:
        if item == element:
            count += 1
    return count

if __name__ == '__main__':
    my_list = [1, 2, 3, 4, 5, 6, 4, 2, 55]
    print(count_element(my_list, 4))
    print(reverse_list(my_list))
    insert_element(my_list, 100, 0)
    print(my_list)
