import math
import random
from .environment import Environment
from .datatypes import OrderedPair
from .bacterium import Bacterium, update_velocity


def initialize_environment(
    num_attackers: int,
    num_targets: int,
    width: float,
    max_bacterium_speed: float,
    proximity: float,
    contact_distance: float,
    mean_run_time: float,
    motility_speed: float,
    seed: int | None = None,
) -> Environment:
    """
    Create an initial snapshot using the HW1 sampling pattern. Author/reviewer: TODO.

    Sample each position coordinate uniformly in [0, width] and each velocity
    component in [-initial_velocity_range, initial_velocity_range]. Set initial
    acceleration to OrderedPair(0.0, 0.0) and alive to True. Apply the speed limit.
    Use a local random.Random(seed) generator for repeatable initial states.
    Return one Environment containing num_attackers + num_targets agents.
    """
    if num_attackers < 0 or num_targets < 0:
        raise ValueError("Bacteria counts must be non-negative integers.")

    if width <= 0:
        raise ValueError("Width must be a positive number.")
    if mean_run_time <= 0:
        raise ValueError("Mean run time must be a positive number.")
    if not 0 <= motility_speed <= max_bacterium_speed:
        raise ValueError("Motility speed must be in [0, max_bacterium_speed].")
    if proximity < 0 or contact_distance < 0:
        raise ValueError("Proximity and contact distance must be non-negative numbers.")

    # random generator
    rng = random.Random(seed)

    bacteria = []


    #  establish empty environment first
    environment = Environment(
        width=width,
        bacteria=bacteria,
        max_bacterium_speed=max_bacterium_speed,
        proximity=proximity,
        contact_distance=contact_distance,
        mean_run_time=mean_run_time,
        motility_speed=motility_speed
    )


    #  initialize bacteria (attacker & target)

    for bacteria_type, count in (
        ("attacker", num_attackers),
        ("target", num_targets),
    ):
        for _ in range(count):
            bacterium = Bacterium(
                position=OrderedPair(
                    rng.uniform(0, width),
                    rng.uniform(0, width),
                ),
                orientation=rng.uniform(0.0, 2 * math.pi),
                bacteria_type=bacteria_type,
                alive=True,
                is_division=False,
            )

            bacterium.velocity = update_velocity(
                bacterium,
                motility_speed,
                max_bacterium_speed,
            )

            environment.bacteria.append(bacterium)

    return environment
