from pathlib import Path

from src.initialization import initialize_environment
from src.simulation import simulate_bacteria
from src.visualization import animate_system


def main() -> None:
    """
    Initialize, simulate, and render, following HW1 main.py. Author/reviewer: TODO.
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
    contact_distance = 10.0
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
    images = animate_system(time_points, canvas_width, drawing_frequency)

    # Count living and dead bacteria in the final snapshot
    final_environment = time_points[-1]

    dead_bacteria = 0
    alive_bacteria = 0

    for bacterium in final_environment.bacteria:
        if bacterium.alive:
            alive_bacteria += 1
        else:
            dead_bacteria += 1
            
    print(f"Total bacteria: {len(final_environment.bacteria)}")
    print(f"Alive bacteria: {alive_bacteria}")
    print(f"Dead bacteria: {dead_bacteria}")

    # Same video-export step as HW1, using the rendered RGB arrays.
    import imageio.v2 as imageio

    Path("outputs").mkdir(exist_ok=True)
    imageio.mimsave("outputs/basic_simulation.mp4", images, fps=30)


if __name__ == "__main__":
    main()
