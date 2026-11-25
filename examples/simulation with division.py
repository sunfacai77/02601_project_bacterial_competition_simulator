from pathlib import Path

from src.initialization import initialize_environment
from src.simulation import simulate_bacteria
from src.visualization import animate_system


def main() -> None:
    """
    Run the standard simulation settings and report bacterial division.
    """
    # HW1 demo settings; these are not calibrated bacterial parameters.
    width = 2000.0
    max_bacterium_speed = 120.0
    proximity = 300.0
    num_gens = 200
    time_step = 0.1
    canvas_width = 600
    drawing_frequency = 2

    # Project-specific demo choices, to be agreed on by the group.
    num_attackers = 25
    num_targets = 25
    contact_distance = 15
    motility_speed = 80
    mean_run_time = 1.0

    initial_environment = initialize_environment(
        num_attackers=num_attackers,
        num_targets=num_targets,
        width=width,
        max_bacterium_speed=max_bacterium_speed,
        proximity=proximity,
        contact_distance=contact_distance,
        mean_run_time=mean_run_time,
        motility_speed=motility_speed,
        seed=42,
    )
    time_points = simulate_bacteria(initial_environment, num_gens, time_step)
    initial_count = len(initial_environment.bacteria)
    alive_count = sum(bacterium.alive for bacterium in initial_environment.bacteria)
    newborn_count = 0
    first_division_step = None

    for step, environment in enumerate(time_points[1:], start=1):
        previous_alive_count = alive_count
        alive_count = sum(bacterium.alive for bacterium in environment.bacteria)
        newly_dead = sum(
            not bacterium.alive and bacterium.time_since_death == 0.0
            for bacterium in environment.bacteria
        )
        # Add back this step's deaths to recover the number of births.
        births = alive_count + newly_dead - previous_alive_count
        newborn_count += births
        if births > 0 and first_division_step is None:
            first_division_step = step

    final_bacteria = time_points[-1].bacteria
    print(f"Initial bacteria: {initial_count}")
    print(f"Newborn bacteria: {newborn_count}")

    print(f"Alive bacteria: {alive_count}")
    print(f"Dead bacteria still present: {len(final_bacteria) - alive_count}")
    if first_division_step is None:
        print("No division completed during the simulation.")
    else:
        print(
            f"First completed division at step {first_division_step} "
            f"(time {first_division_step * time_step:.1f})."
        )

    images = animate_system(time_points, canvas_width, drawing_frequency)


    import imageio.v2 as imageio

    Path("outputs").mkdir(exist_ok=True)
    imageio.mimsave("outputs/simulation_with_division.mp4", images, fps=30)


if __name__ == "__main__":
    main()
