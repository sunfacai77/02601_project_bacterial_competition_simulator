# Bacterial Competition Simulator

Our final project for 02601 builds on the Sky and Boids simulations from class. We are developing a Python model of bacteria competing on a two-dimensional surface. Each bacterium is an individual agent, and we want to explore how movement and local contact affect the survival of attacker and target populations.

We plan to use biological mechanisms and parameters from the literature to guide the model. The first step is to get a small simulation working before adding more detailed biology.

## Where we are now

This repository currently contains the project skeleton: data classes, function interfaces, a planned example, and space for tests. The simulation logic has **not been implemented yet**.

For Checkpoint 1, our goal is to:

- Create attacker and target bacteria and place them in an environment.
- Move them through a sequence of time steps and handle the boundaries.
- Add a simple contact-killing rule and plot the population in space.


## Repository layout

```text
src/
    __init__.py
    datatypes.py          # OrderedPair, shared by positions and motion vectors
    bacterium.py          # Bacterium and motion/vector helpers
    environment.py        # Environment, copy_environment, update_environment
    initialization.py     # Build the initial population
    interactions.py       # Contact detection and killing
    simulation.py         # simulate_bacteria and the list of time points
    visualization.py      # animate_system, draw_to_canvas, draw_bacterium
examples/
    __init__.py
    basic_simulation.py   # Intended entry point once the core is ready
tests/
    test_bacterium.py
    test_environment.py
    test_interactions.py
    test_simulation.py
requirements.txt
```

The flow follows our homework: create an initial state, simulate a list of time points, then render the saved states. 

## First round of work

| Owner | Main responsibility | Suggested branch |
| --- | --- | --- |
| Member 1 | `Bacterium`, motion updates, speed limits, and vector helpers |
| Member 2 | `Environment`, copying and updating snapshots, initialization, and boundaries |
| Member 3 | Contact detection, simple killing, and visualization |
| All three | Connect the modules through `simulate_bacteria`, finish the example, and check the results |

Each person should add tests for their own part.

## Shared interface

- Positions, velocities, and accelerations are `OrderedPair` objects, accessed through `.x` and `.y`, as in both assignments. Dataclass vector and list fields use `default_factory` so agents do not share mutable defaults.
- `bacteria_type` is either `"attacker"` or `"target"`. Every bacterium has an `alive` flag.
- `Environment.bacteria` stores both living and dead bacteria. Dead bacteria remain available for bookkeeping but do not move or participate in contacts. The first renderer will draw living bacteria only.
- Motion follows the HW1 interfaces: compute new acceleration from the current environment; update velocity using the average of old and new acceleration, then limit speed; update position using old velocity and old acceleration. Save independent copies of those old vectors before assigning updates. Motion helpers return values for the caller to assign.
- The surface is a square spanning `[0, width]` on both axes. `update_position` wraps coordinates around the boundaries, following Boids. `in_field` is the bounds-check interface from Barnes-Hut; it does not remove agents.
- `proximity` is a neighborhood threshold for future movement rules. `contact_distance` is a separate bacterial interaction parameter. The Boids separation, alignment, and cohesion rules and the Barnes-Hut gravity/quadtree algorithm are not part of the initial bacterial model.
- For the initial point-agent model, contact means ordinary Euclidean `distance(p0, p1) <= environment.contact_distance`. `detect_contacts(environment)` returns each living pair once. This follows HW1's distance convention: opposite edges are not treated as neighboring points despite wrap-around movement. We may revisit that choice for later experiments.
- `kill_target(attacker, target)` is the simple first rule: mark a living target dead after contact. `resolve_killing` selects attacker-target pairs from the detected contacts. Probability models can replace this later.
- `initialize_environment` creates the initial agents and settings. `update_environment` copies a snapshot, updates living agents, then detects contacts and resolves killing on the new copy. All movement decisions read the old state.
- `simulate_bacteria` returns `num_gens + 1` independent snapshots in `time_points`, starting with the initial environment. Snapshot `i` represents time `i * time_step`. Copy every agent and vector so future updates and killing cannot change earlier states.
- `animate_system(time_points, canvas_width, drawing_frequency)` renders saved snapshots without advancing the simulation. It returns RGB NumPy arrays for imageio, as in HW1. Population curves can later be computed by counting living attackers and targets in each snapshot.

The signatures and docstrings in `src/` describe these interfaces.

The example uses HW1 settings: `width=2000.0`, `max_bacterium_speed=120.0`, `proximity=300.0`, initial velocity components in `[-60, 60]`, `num_gens=200`, `time_step=0.1`, `canvas_width=600`, `drawing_frequency=2`, and video output at 30 fps. The split into 25 attackers and 25 targets, `contact_distance=10.0`, and `seed=42` are project demo choices. These numbers are a familiar debugging starting point; physical units and bacterial parameters still need to be chosen.
