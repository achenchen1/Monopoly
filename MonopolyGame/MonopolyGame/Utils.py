from __future__ import annotations
from typing import Dict, List, Optional, Any


class Ring:
    class Node:
        def __init__(self, value, left, right) -> None:
            self.right: Ring.Node = right  # next
            self.left: Ring.Node = left  # prev
            self.value: Any = value

        def __hash__(self) -> int:
            return self.value.__hash__()

        def __repr__(self) -> str:
            return repr(self.value)

        def __str__(self) -> str:
            return str(self.value)

    def __len__(self):
        return self.size()

    def __init__(self, base: List[Any]) -> None:
        self.size: int = 0
        self.hashed: Dict[Any, Ring.Node] = {}
        self.head = None

        prev_node: Optional[Ring.Node] = None

        for i in base:
            new_node: Ring.Node = Ring.Node(i, prev_node, None)
            if prev_node is not None:
                prev_node.right = new_node
            else:
                self.head = new_node
            prev_node = new_node
            self.hashed[i] = new_node
            self.size += 1

        self.head.left = prev_node
        prev_node.right = self.head

    def __iter__(self):
        return self

    def __next__(self) -> Ring.Node:
        if self.size > 0:
            self.head = self.head.right
            return self.head.left
        raise StopIteration

    def __repr__(self) -> str:
        nodes = []
        current = self.head
        for _ in range(self.size):
            nodes.append(current)
            current = current.right
        return " -> ".join(str(n) for n in nodes)

    def __str__(self) -> str:
        return repr(self)

    def append(self, value: Any):
        new_node = Ring.Node(value, self.head.left, self.head)
        self.head.left.right = new_node
        self.head.left = new_node
        self.size += 1

    def remove(self):
        # TODO
        pass