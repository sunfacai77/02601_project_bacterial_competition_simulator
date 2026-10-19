from dataclasses import dataclass


@dataclass
class OrderedPair:
    """
    Represents a point or vector in two-dimensional space.

    Attributes:
        x (float): The x-coordinate of the point or vector.
        y (float): The y-coordinate of the point or vector.
    """

    x: float = 0.0
    y: float = 0.0
