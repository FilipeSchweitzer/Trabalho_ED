# src/search.py
from typing import List, Any

def linear_search(arr: List[Any], x: Any) -> int:
    """
    Busca linear (O(n)).
    Retorna o índice se encontrado, senão -1.
    """
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

def binary_search(arr: List[Any], x: Any) -> int:
    """
    Busca binária (O(log n)).
    Assume que 'arr' está ordenada. Retorna o índice se encontrado, senão -1.
    """
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (high + low) // 2
        # É importante que os elementos em 'arr' suportem comparação (<, >)
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1