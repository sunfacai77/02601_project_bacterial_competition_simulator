from dataclasses import dataclass, field

from .bacterium import Bacterium
from .datatypes import OrderedPair


@dataclass
class Environment:
    """
    A square surface containing the bacteria at a single time point.

    Attributes:
        width: Side length of the square, following Sky.width / Universe.width.
        bacteria: Living and dead agents in this snapshot.
        max_bacterium_speed: Speed limit, corresponding to max_boid_speed.
        proximity: Neighborhood distance for future movement rules, as in HW1.
        contact_distance: Separate threshold for bacterial contact and killing.

    Defaults follow the zero/empty dataclass style of the homework. Set actual
    simulation parameters during initialization; they are not biological units.
    """

    width: float = 0.0
    bacteria: list[Bacterium] = field(default_factory=list)
    max_bacterium_speed: float = 0.0
    proximity: float = 0.0
    contact_distance: float = 0.0

    def in_field(self, p: OrderedPair) -> bool:
        """
        Check [0, width] x [0, width], as in Universe.in_field. Author/reviewer: TODO.
        """
        raise NotImplementedError("Implement the bounds check.")


def copy_environment(current_environment: Environment) -> Environment:
    """
    Return an independent copy, as in copy_sky/copy_universe. Author/reviewer: TODO.

    Copy every parameter and bacterium, including alive and bacteria_type.
    Allocate new OrderedPair objects for position, velocity, and acceleration.
    Mutating the copy must not change any previous time point.
    """
    raise NotImplementedError("Implement snapshot copying.")


def update_environment(
    current_environment: Environment,
    time_step: float,
) -> Environment:
    """
    Return the next snapshot, as in update_sky/update_universe. Author/reviewer: TODO.

    Copy the current environment first. For each living agent, preserve its old
    acceleration and velocity, compute acceleration from current_environment,
    then assign update_velocity and update_position results to the copied agent.
    After all motion is complete, detect contacts and resolve killing on the copy.
    Dead agents remain stored and stationary. Never mutate current_environment.
    """
    raise NotImplementedError("Implement one environment update.")
