from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from .datatypes import OrderedPair

if TYPE_CHECKING:
    from .environment import Environment


BacteriaType = Literal["attacker", "target"]


@dataclass
class Bacterium:
    """
    An individual agent, corresponding to Boid in HW1 and Star in HW2.

    Each agent has position, velocity, and acceleration as OrderedPair objects.
    bacteria_type and alive are additional state for bacterial competition.
    """

    position: OrderedPair = field(default_factory=OrderedPair)
    velocity: OrderedPair = field(default_factory=OrderedPair)
    acceleration: OrderedPair = field(default_factory=OrderedPair)
    bacteria_type: BacteriaType = "target"
    alive: bool = True


def update_acceleration(current_environment: Environment, i: int) -> OrderedPair:
    """
    Compute the next acceleration of bacteria[i]. Author/reviewer: TODO.

    Read neighbors from current_environment, as update_acceleration reads
    current_sky in HW1. The bacterial movement rule is still to be decided;
    zero acceleration is sufficient for an initial constant-velocity demo.
    """
    raise NotImplementedError("Implement bacterial acceleration.")


def update_velocity(
    b: Bacterium,
    old_acceleration: OrderedPair,
    max_bacterium_speed: float,
    time_step: float,
) -> OrderedPair:
    """
    Return velocity using the HW1 averaged-acceleration rule. Author/reviewer: TODO.

    Use b.velocity + 0.5 * (old_acceleration + b.acceleration) * time_step,
    then limit_speed. b.acceleration is the newly computed acceleration.
    Do not mutate b or its vectors; the caller assigns the result.
    """
    raise NotImplementedError("Implement the velocity update.")


def update_position(
    b: Bacterium,
    old_acceleration: OrderedPair,
    old_velocity: OrderedPair,
    environment_width: float,
    time_step: float,
) -> OrderedPair:
    """
    Return position with HW1 wrap-around boundaries. Author/reviewer: TODO.

    Use b.position + old_velocity * time_step
    + 0.5 * old_acceleration * time_step**2, independently for x and y.
    Wrap each coordinate into [0, environment_width], including overshoots
    larger than one width. Leave b and its vectors unchanged.
    """
    raise NotImplementedError("Implement the position update and wrap-around.")


def limit_speed(vel: OrderedPair, max_speed: float) -> OrderedPair:
    """
    Return a vector limited to max_speed without changing vel. Author/reviewer: TODO.
    """
    raise NotImplementedError("Implement the speed limit.")


def sum_vectors(vectors: list[OrderedPair]) -> OrderedPair:
    """
    Return the sum of 2-D vectors, as in HW1. Author/reviewer: TODO.
    """
    raise NotImplementedError("Implement vector summation.")


def distance(p0: OrderedPair, p1: OrderedPair) -> float:
    """
    Return Euclidean distance between two points, as in HW1. Author/reviewer: TODO.
    """
    raise NotImplementedError("Implement the distance calculation.")
