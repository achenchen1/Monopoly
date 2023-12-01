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
            return f"Node({repr(self.value)})"

        def __str__(self) -> str:
            return f"Node({str(self.value)})"

    def __len__(self):
        return self.size

    def __init__(self, base: List[Any]) -> None:
        self.size: int = 0
        self.hashed: Dict[Any, Ring.Node] = {}
        self.head = None
        self.iterator = None

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
        if self.iterator != None:
            # https://stackoverflow.com/questions/46941719/how-can-i-have-multiple-iterators-over-a-single-python-iterable-at-the-same-time
            raise NotImplementedError("Need to add a separate iterator class")
        self.iterator = self.head
        return self

    def __next__(self) -> Ring.Node:
        if self.size > 0:
            to_return = self.iterator
            self.iterator = self.iterator.right
            return to_return.value
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

    def append(self, value: Any) -> None:
        new_node = Ring.Node(value, self.head.left, self.head)
        self.hashed[value] = new_node
        self.head.left.right = new_node
        self.head.left = new_node
        self.size += 1

    def pop(self, value: Any) -> Any:
        # if we remove the head, set head to the next node
        # it's fine if we remove the self.iterator node; it's not like we're free()ing the memory for it.
        if value not in self.hashed:
            raise ValueError(
                f"Can't pop {value}, value is not in Ring - values in Ring: {self.hashed}"
            )
        if self.head.value == value:
            self.head = self.head.right

        to_remove = self.hashed[value]
        to_remove.left.right = to_remove.right
        to_remove.right.left = to_remove.left
        self.size -= 1

        return self.hashed.pop(value)

    def set_head(self, value: Any) -> Any:
        if value not in self.hashed:
            raise ValueError(
                f"Can't set head to {value}, value is not in Ring - values in Ring: {self.hashed}"
            )
        else:
            self.head = self.hashed[value]
            return self.head
