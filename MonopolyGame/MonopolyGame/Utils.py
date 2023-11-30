from typing import Set, List, Optional


class PlayerCycler:
    class Node:
        def __init__(self, value, left, right) -> None:
            self.right: PlayerCycler.Node = right  # next
            self.left: PlayerCycler.Node = left  # prev
            self.value: int = value

        def __hash__(self) -> int:
            return self.value

    def __init__(self, base: List[int]) -> None:
        self.total: int = 0
        self._hashed: Set = set()
        self.head = None

        prev_node: Optional[PlayerCycler.Node] = None
        for i in base:
            new_node: PlayerCycler.Node = PlayerCycler.Node(i, prev_node, None)
            if prev_node is not None:
                prev_node.right = new_node
            else:
                self.head = new_node
            prev_node = new_node
        self.tail = prev_node

        self.head.left = self.tail
        self.tail.right = self.head
