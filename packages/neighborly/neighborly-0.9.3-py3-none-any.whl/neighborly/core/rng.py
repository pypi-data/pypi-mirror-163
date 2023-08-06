import random
from abc import abstractmethod
from typing import List, MutableSequence, Optional, Protocol, Sequence, TypeVar

_T = TypeVar("_T")


class IRandNumGenerator(Protocol):
    """Abstract interface for a class that handles generating random numbers"""

    @abstractmethod
    def random(self) -> float:
        """Return a random float between [0.0, 1.0] inclusive"""
        raise NotImplementedError()

    @abstractmethod
    def choice(self, s: Sequence[_T]) -> _T:
        """Return an item from this sequence"""
        raise NotImplementedError()

    @abstractmethod
    def choices(
        self,
        s: Sequence[_T],
        weights: Optional[List[int]] = None,
        cum_weights: Optional[List[int]] = None,
        k: int = 1,
    ) -> List[_T]:
        """Return one or more items from a sequence using weighted random selection"""
        raise NotImplementedError()

    @abstractmethod
    def sample(self, s: Sequence[_T], n: int) -> List[_T]:
        """Return an n-number of random items from the sequence"""
        raise NotImplementedError()

    @abstractmethod
    def normal(self, mu: float, sigma: float) -> float:
        """Return an item from this sequence"""
        raise NotImplementedError()

    @abstractmethod
    def uniform(self, low: float, high: float) -> float:
        """Return an item from this sequence"""
        raise NotImplementedError()

    @abstractmethod
    def randint(self, low: int, high: int) -> int:
        """Return an item from this sequence"""
        raise NotImplementedError()

    @abstractmethod
    def shuffle(self, seq: MutableSequence) -> None:
        """Shuffle the items in a sequence"""
        raise NotImplementedError()


class DefaultRNG:
    """Default RNG that wraps an instance of Python's random"""

    __slots__ = "_rng"

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng: random.Random = random.Random(seed)

    def random(self) -> float:
        """Return a random float between [0.0, 1.0] inclusive"""
        return self._rng.random()

    def choice(self, s: Sequence[_T]) -> _T:
        """Return an item from this sequence"""
        return self._rng.choice(s)

    def choices(
        self,
        s: Sequence[_T],
        weights: Optional[List[int]] = None,
        cum_weights: Optional[List[int]] = None,
        k: int = 1,
    ) -> List[_T]:
        """Return one or more items from a sequence using weighted random selection"""
        return self._rng.choices(s, weights=weights, cum_weights=cum_weights, k=k)

    def sample(self, s: Sequence[_T], n: int) -> List[_T]:
        """Return an n-number of random items from the sequence"""
        return self._rng.sample(s, k=n)

    def normal(self, mu: float, sigma: float) -> float:
        """Return an item from this sequence"""
        return self._rng.gauss(mu, sigma)

    def uniform(self, low: float, high: float) -> float:
        """Return an item from this sequence"""
        return self._rng.uniform(low, high)

    def randint(self, low: int, high: int) -> int:
        """Return an item from this sequence"""
        return self._rng.randint(low, high)

    def shuffle(self, seq: MutableSequence) -> None:
        self._rng.shuffle(seq)
