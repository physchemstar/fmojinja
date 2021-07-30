from typing import List, Any


def broadcast_n(n: int):
    def broadcast(values: List[Any], onedex: int) -> Any:
        if len(values) == 1:
            return values[0]
        if len(values) != n:
            raise ValueError(f"The numbers doesn't match. expected {n} or 1, exact {len(values)}.")
        return values[onedex - 1]
    return broadcast
