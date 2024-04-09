from bitstring import Bits
from dataclasses import dataclass
from functools import lru_cache
from typing import AnyStr, Dict, Iterable, Union, Tuple, TypeVar, Generic

_T = TypeVar("_T")


@dataclass
class HuffmanTree(Generic[_T]):
    """
    Huffman coding tree
    """

    frequency: int
    "The frequency of this symbol appeared in the corpus"

    symbol: Union[_T, None] = None
    "The symbol of this tree (leaf node)"

    left: Union["HuffmanTree[_T]", None] = None
    "The left child of this tree (internal node)"

    right: Union["HuffmanTree[_T]", None] = None
    "The right child of this tree (internal node)"

    @staticmethod
    def from_symbolic_frequencies(
        values: Iterable[Tuple[int, _T]]
    ) -> "HuffmanTree[_T]":
        """
        Create a Huffman tree from frequencies with their symbols

        ## Parameters
        - `values`: An iterable of tuples of frequencies and symbols

        ## Returns
        - A Huffman tree
        """
        from heapq import heapify, heappush, heappop

        values = sorted(map(lambda args: HuffmanTree(*args), values))
        heapify(values)

        while len(values) > 1:
            heappush(values, (heappop(values)) + heappop(values))
        return values[0]

    def decode(self, code: Bits) -> Tuple[_T, Bits]:
        """
        Decode a Huffman code into a symbol

        ## Parameters
        - `code`: The Huffman code to decode
            - If the *prefix* does not match any code,
              a `ValueError` will be raised.

        ## Returns
        - A tuple of the symbol and the remaining code
        """

        try:
            return self._decode(code)
        except ValueError:
            raise ValueError(f"Unrecognized code: {code}")

    def encode(self, symbol: _T) -> Bits:
        """
        Encode a symbol into a Huffman code

        ## Parameters
        - `symbol`: The symbol to encode

        ## Returns
        - The Huffman code of the symbol as `Bits`
        """

        return self._get_codetable()[symbol]

    def equal(self, other: "HuffmanTree[_T]") -> bool:
        """
        Fully compare two Huffman trees
        """

        result = self.frequency == other.frequency and self.symbol == other.symbol

        if self.left and other.left:
            result = result and self.left.equal(other.left)
        elif not self.left and not other.left:
            result = result and True

        if self.right and other.right:
            result = result and self.right.equal(other.right)
        elif not self.right and not other.right:
            result = result and True
        return result

    def _decode(self, prefix: Bits) -> Tuple[_T, Bits]:
        """
        An internal method of `HuffmanTree.decode`
        """

        if not self.left and not self.right:
            return (self.symbol, prefix)
        if not prefix:
            raise ValueError()

        if prefix[0]:
            if self.right:
                return self.right._decode(prefix[1:])
        elif self.left:
            return self.left._decode(prefix[1:])
        else:
            raise ValueError()

    # @lru_cache(maxsize=1)
    def _get_codetable(self) -> Dict[_T, Bits]:
        """
        An internal method of `HuffmanTree.encode`
        """

        return dict(self._get_codetable_2(Bits()))

    def _get_codetable_2(self, prefix: Bits) -> Iterable[Tuple[_T, Bits]]:
        """
        An internal method of `HuffmanTree._get_codetable`
        """

        if not self.left and not self.right:
            yield (self.symbol, prefix)
        if self.left:
            yield from self.left._get_codetable_2(prefix + Bits(bin="0"))
        if self.right:
            yield from self.right._get_codetable_2(prefix + Bits(bin="1"))

    def _repr(self) -> str:
        """
        An internal method of `HuffmanTree.__repr__`
        """
        symbol_repr = f":{self.symbol}" if self.symbol else ""
        node_repr = f"{self.frequency}{symbol_repr}"
        left_repr = f"{self.left._repr()}" if self.left else ""
        right_repr = f"{self.right._repr()}" if self.right else ""
        left_symbol_repr = (
            f":{self.left.symbol}" if self.left and self.left.symbol else ""
        )
        right_symbol_repr = (
            f":{self.right.symbol}" if self.right and self.right.symbol else ""
        )
        left_node_repr = (
            f" --> {self.left.frequency}{left_symbol_repr}" if self.left else ""
        )
        right_node_repr = (
            f" --> {self.right.frequency}{right_symbol_repr}" if self.right else ""
        )
        if not self.left and not self.right:
            return f"""\
    {node_repr}
"""
        return f"""\
    {node_repr}{left_node_repr}
    {node_repr}{right_node_repr}
{left_repr}{right_repr}"""

    def __eq__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency == other.frequency

    def __ge__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency >= other.frequency

    def __gt__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency > other.frequency

    def __le__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency <= other.frequency

    def __lt__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency < other.frequency

    def __ne__(self, other: "HuffmanTree[_T]") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency != other.frequency

    def __add__(self, other: "HuffmanTree[_T]") -> "HuffmanTree[_T]":
        """
        Add the frequencies of two Huffman nodes,
        and return a new tree with the two nodes as children.
        """

        return HuffmanTree(self.frequency + other.frequency, None, self, other)

    def __repr__(self) -> str:
        """
        Represents information of the tree:

        1. The Huffman code table in Python syntax
        2. The Huffman tree in Mermaid diagram syntax
        """

        from pprint import pformat

        return f"""\
```python
{pformat(self._get_codetable())}
```

```mermaid
graph TD
{self._repr()}
```"""
