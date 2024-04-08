from bitarray import bitarray
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

    left: Union["HuffmanTree", None] = None
    "The left child of this tree (internal node)"

    right: Union["HuffmanTree", None] = None
    "The right child of this tree (internal node)"

    @staticmethod
    def from_symbolic_frequencies(values: Iterable[Tuple[int, _T]]) -> "HuffmanTree":
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
    def codebook(self) -> Iterable[Tuple[_T, bitarray]]:
        """
        Get the codebook of the Huffman tree

        ## Returns
        - An iterable of tuples of symbols
          and their Huffman codes represented as `bitarray`
        """

        return self._get_codebook(bitarray())

    def _get_codebook(self, prefix: bitarray) -> Iterable[Tuple[_T, bitarray]]:
        """
        Internal method of `HuffmanTree.codebook`
        """

        if not self.left and not self.right:
            yield (self.symbol, prefix)
        if self.left:
            yield from self.left._get_codebook(prefix + "0")
        if self.right:
            yield from self.right._get_codebook(prefix + "1")

    def __eq__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency == other.frequency

    def __ge__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency >= other.frequency

    def __gt__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency > other.frequency

    def __le__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency <= other.frequency

    def __lt__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency < other.frequency

    def __ne__(self, other: "HuffmanTree") -> bool:
        "Compare the frequencies of two Huffman trees"
        return self.frequency != other.frequency

    def __add__(self, other: "HuffmanTree") -> "HuffmanTree":
        """
        Add the frequencies of two Huffman nodes,
        and return a new tree with the two nodes as children.
        """
        return HuffmanTree(self.frequency + other.frequency, None, self, other)
