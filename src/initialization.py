from .environment import Environment


def initialize_environment(
    num_attackers: int,
    num_targets: int,
    width: float,
    max_bacterium_speed: float,
    proximity: float,
    contact_distance: float,
    initial_velocity_range: float = 60.0,
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
    raise NotImplementedError("Implement initial population generation.")
