from .environment import Environment
from environment import update_environment

def simulate_bacteria(
    initial_environment: Environment,
    num_gens: int,
    time_step: float,
) -> list[Environment]:
    """
    Return the initial state and num_gens updated states. Author/reviewer: TODO.

    Follow simulate_boids(initial_sky, num_gens, time_step): start time_points
    with initial_environment, then repeatedly call update_environment on the
    last state. Return num_gens + 1 snapshots; num_gens=0 returns just the initial
    state. No snapshot may share mutable agents or vectors with another.
    Snapshot i represents time i * time_step. Initial state generation is separate.
    """
    result = [initial_environment]
    for i in range(0, num_gens):
        result.append(update_environment(result[i], time_step))

    return result
