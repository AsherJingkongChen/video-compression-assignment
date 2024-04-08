from dataclasses import dataclass
from typing import Iterable, Union, Tuple, TypeVar, Generic

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

    @property
    def codebook(self) -> Iterable[Tuple[_T, str]]:
        """
        Get the codebook of the Huffman tree

        ## Returns
        - An iterable of tuples of symbols
          and their Huffman codes represented as `str`
        """

        return self._get_codebook("")

    def _get_codebook(self, prefix: str) -> Iterable[Tuple[_T, str]]:
        """
        Internal method of `HuffmanTree.codebook`
        """

        if not self.left and not self.right:
            yield (self.symbol, prefix)
        if self.left:
            yield from self.left._get_codebook(prefix + "0")
        if self.right:
            yield from self.right._get_codebook(prefix + "1")

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
        Represents the Huffman tree in Mermaid diagram syntax
        """
        symbol_repr = f":{self.symbol}" if self.symbol else ""
        node_repr = f"{self.frequency}{symbol_repr}"
        left_repr = f"{self.left}" if self.left else ""
        left_symbol_repr = (
            f":{self.left.symbol}" if self.left and self.left.symbol else ""
        )
        left_node_repr = (
            f" --> {self.left.frequency}{left_symbol_repr}" if self.left else ""
        )
        right_repr = f"{self.right}" if self.right else ""
        right_symbol_repr = (
            f":{self.right.symbol}" if self.right and self.right.symbol else ""
        )
        right_node_repr = (
            f" --> {self.right.frequency}{right_symbol_repr}" if self.right else ""
        )
        return f"""\
    {node_repr}{left_node_repr}
    {node_repr}{right_node_repr}
{left_repr}{right_repr}"""