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
    *,
    layout: str = "uniform",
    crowding_radius: float = 0.0,
    crowding_threshold: int = 0,
    crowded_speed_factor: float = 1.0,
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
    if layout not in ("uniform", "mixed_clusters", "separated_clusters"):
        raise ValueError(f"Unknown initial layout:{layout}")
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
        motility_speed=motility_speed,
        crowding_radius=crowding_radius,
        crowding_threshold=crowding_threshold,
        crowded_speed_factor=crowded_speed_factor,
    )


    #  initialize bacteria (attacker & target)
    #  outer loop: iterate over bacteria culster center for attackers and targets
    #      inner loop: iterate over number of bacteria individually and assign position


    # uniform layout: sample each position coordinate uniformly in [0, width]
    # mixed cluster layout: sample each position coordinate uniformly in...
    # seperated clusters layout: sample center of cluster at the same level(same center_y, diiferent center_x) 
    # and sample each position coordinate uniformly in [center_x - cluster_radius, center_x + cluster_radius] and [center_y - cluster_radius, center_y + cluster_radius]

    center_y = width / 2
    spread = 0.06 * width      #? standaerd deviation of the cluster distribution(可调整)

    for bacteria_type, count in (
        ("attacker", num_attackers),
        ("target", num_targets),
    ):
        center_x = width / 2
       
        for _ in range(count):
            if layout == "uniform":
                position = OrderedPair(
                    rng.uniform(0, width),
                    rng.uniform(0, width),
                )

            elif layout == "mixed_clusters":
                while True:
                    position = OrderedPair(
                        rng.gauss(center_x, spread),
                        rng.gauss(center_y, spread),
                    )
                    if environment.in_field(position):      # check if the position is within the env field
                        break                               # valid, break the loop, otherwise resample(while True loop)


            elif layout == "separated_clusters":
                if bacteria_type == "attacker":
                    center_x = width / 4        # seperate attacker at left mid

                else:
                    center_x = 3 * width / 4      # seperate target at right mid

                while True:
                    position = OrderedPair(
                        rng.gauss(center_x, spread),
                        rng.gauss(center_y, spread),
                    )
                    if environment.in_field(position):
                        break                               
                
            bacterium = Bacterium(
                position=position,
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
