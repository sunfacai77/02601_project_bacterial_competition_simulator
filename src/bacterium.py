from __future__ import annotations

import math
import random
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

    # basic para, we do not need acceleration here (see bacteria notes)
    position: OrderedPair = field(default_factory=OrderedPair)
    velocity: OrderedPair = field(default_factory=OrderedPair)
    # movement direction in radians. sample uniformly from [0, 2*pi) during initialization
    orientation: float = 0.0
    
    
    bacteria_type: BacteriaType | None = None
    
    # HP value. every hit will reduce the target's HP by some random value. 
    health: float | None = None
    # die when HP <= 0
    alive: bool = True
    
    # energy is associated with environment setting. assume every bacterium has the same energy recovery rate
    energy: float | None = None
    energy_recovery_rate: float | None = None # can be set to constant
    
    # growth rate is for energy distribution. it will change when energy is high or low
    growth_rate: float | None = None
    # when growth stage reaches growth threshold, the bacterium will divide into two
    growth_stage: float | None = None
    growth_threshold: float | None = None # can be set to constant
    
    # during division, there will be a period of time when the bacterium is not able to move or attack. 
    is_division: bool = False
    division_time: float | None = None # can be set to constant

    
    # may be used
    radius: float | None = None



def update_orientation(
    b: Bacterium,
    mean_run_time: float,
    time_step: float,
    rng: random.Random | None = None,
) -> float:
    """
    Update the movement direction of a bacterium.

    Args:
        b: A Bacterium object.
        mean_run_time: The mean time before choosing a new direction.
        time_step: The time step. Use a value much smaller than mean_run_time.
        rng: An optional random generator for repeatable movement.
    Returns:
        The updated direction in radians. Dead or dividing bacteria keep
        their current direction. Leave b unchanged; the caller assigns the result.
    Raises:
        ValueError: If mean_run_time is not positive or time_step is negative.
    """
    if not b.alive or (b.health is not None and b.health <= 0) or b.is_division:
        return b.orientation

    if mean_run_time <= 0:
        raise ValueError("Mean run time must be positive.")
    if time_step < 0:
        raise ValueError("Time step must be nonnegative.")
    if time_step == 0:
        return b.orientation

    generator = rng if rng is not None else random

    # probability of turning in one time step: 1 - exp(-time_step / mean_run_time)
    turning_probability = -math.expm1(-time_step / mean_run_time)
    if generator.random() < turning_probability:
        return generator.uniform(0.0, 2 * math.pi)

    return b.orientation


def update_velocity(
    b: Bacterium,
    motility_speed: float,
    max_bacterium_speed: float,
) -> OrderedPair:
    """
    Update the velocity of a bacterium.

    Args:
        b: A Bacterium object.
        motility_speed: The constant movement speed, shared by all moving bacteria.
        max_bacterium_speed: The maximum allowed speed of the bacterium.
    Returns:
        An OrderedPair representing the velocity in the updated direction,
        limited to max_bacterium_speed. Dead or dividing bacteria return zero velocity.
    Raises:
        ValueError: If motility_speed or max_bacterium_speed is negative.

    Assign update_orientation's result to b.orientation before calling this function.
    Set motility_speed at or below max_bacterium_speed. Leave b and its vectors
    unchanged; the caller assigns the result.
    """
    if not b.alive or (b.health is not None and b.health <= 0) or b.is_division:
        return OrderedPair(0.0, 0.0)

    if motility_speed < 0:
        raise ValueError("Motility speed must be nonnegative.")

    # here add orientation!
    new_x = motility_speed * math.cos(b.orientation)
    new_y = motility_speed * math.sin(b.orientation)

    return limit_speed(OrderedPair(new_x, new_y), max_bacterium_speed)


def update_position(
    b: Bacterium,
    environment_width: float,
    time_step: float,
) -> OrderedPair:
    """
    Update the position of a bacterium.

    Args:
        b: A Bacterium object.
        environment_width: The width of the environment (used for wrap-around behavior).
        time_step: The time step over which to update the position.
    Returns:
        An OrderedPair representing the updated position of the bacterium after
        time_step seconds.
        Dead or dividing bacteria remain at their current position.
        
        !!!Notice: when hit the boundary, stop at the boundary and choose a random inward direction.
        
    Raises:
        ValueError: If environment_width is not positive or time_step is negative.
    """
    if not b.alive or (b.health is not None and b.health <= 0) or b.is_division:
        return OrderedPair(b.position.x, b.position.y)

    if environment_width <= 0:
        raise ValueError("Environment width must be positive.")
    if time_step < 0:
        raise ValueError("Time step must be nonnegative.")

    # use the updated velocity and wrap coordinates into [0, environment_width)
    # because v is already associated with orientation, we can directly use it to update position
    new_x = b.position.x + b.velocity.x * time_step
    new_y = b.position.y + b.velocity.y * time_step
    
    # check boundary!
    # four cases: left, right, top, bottom
    if (new_x <= 0) or (new_x >= environment_width) or (new_y <= 0) or (new_y >= environment_width):
        # stop at the boundary
        new_x = max(0, min(new_x, environment_width))
        new_y = max(0, min(new_y, environment_width))
        
        # choose a random inward direction
        # have to point inside!
        # speed does not change
        speed = math.sqrt(b.velocity.x**2 + b.velocity.y**2)
        angle = random.uniform(0, 2 * math.pi)
        
        
        # choose angle based on which boundary is hit
        # need consider corner first!!! (two conditions are true)
        # left down
        if new_x == 0 and new_y == 0:
            angle = random.uniform(0, math.pi/2)
        # left up
        elif new_x == 0 and new_y == environment_width:
            angle = random.uniform(-math.pi/2, 0)
        # right down
        elif new_x == environment_width and new_y == 0:
            angle = random.uniform(math.pi/2, math.pi)
        # right up
        elif new_x == environment_width and new_y == environment_width:
            angle = random.uniform(math.pi, 3*math.pi/2)
        # now just one boundary
        # left boundary, point right
        elif new_x == 0:
            angle = random.uniform(-math.pi/2, math.pi/2)
        # right boundary, point left
        elif new_x == environment_width:
            angle = random.uniform(math.pi/2, 3*math.pi/2)
        # bottom boundary, point up
        elif new_y == 0:
            angle = random.uniform(0, math.pi)
        # top boundary, point down
        elif new_y == environment_width:
            angle = random.uniform(math.pi, 2 * math.pi)
        
        # seperate x and y
        # already contrained the angle, so no need to use abs()
        vel_x = speed * math.cos(angle)
        vel_y = speed * math.sin(angle)
        
        # update final one
        b.velocity = OrderedPair(vel_x, vel_y)
        # to maintain the uniformity, turn angle to [0, 2*pi)
        angle = angle % (2 * math.pi)
        b.orientation = angle
        
    return OrderedPair(new_x, new_y)


def limit_speed(vel: OrderedPair, max_speed: float) -> OrderedPair:
    """
    Limit the speed of a bacterium.

    Args:
        max_speed: The maximum allowed speed.
        vel: An OrderedPair representing the velocity vector.
    Returns:
        An OrderedPair representing the velocity after limiting its
        magnitude to max_speed, if necessary. Leave vel unchanged.
    Raises:
        ValueError: If max_speed is negative.
    """
    if max_speed < 0:
        raise ValueError("Maximum speed must be nonnegative.")

    s = math.sqrt(vel.x * vel.x + vel.y * vel.y)
    if s > max_speed:
        scale = max_speed / s
        return OrderedPair(vel.x * scale, vel.y * scale)

    return OrderedPair(vel.x, vel.y)


def sum_vectors(vectors: list[OrderedPair]) -> OrderedPair:
    """
    Sum multiple vectors.

    Args:
        vectors: A list of OrderedPair vectors.
    Returns:
        An OrderedPair representing the sum of all vectors in the list.
    """
    sum_x = 0.0
    sum_y = 0.0

    for vector in vectors:
        sum_x += vector.x
        sum_y += vector.y

    return OrderedPair(sum_x, sum_y)


def distance(p0: OrderedPair, p1: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points in 2D space.
    Input:
        p0 (OrderedPair): The first point, with x and y coordinates.
        p1 (OrderedPair): The second point, with x and y coordinates.
    Output:
        float: The Euclidean distance between p0 and p1.
    """
    dx = p0.x - p1.x
    dy = p0.y - p1.y
    return math.sqrt(dx * dx + dy * dy)
