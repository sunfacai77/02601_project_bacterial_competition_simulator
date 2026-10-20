from __future__ import annotations

from typing import TYPE_CHECKING

from .bacterium import Bacterium
from .environment import Environment

import numpy as np
import pygame


def animate_system(
    time_points: list[Environment],
    canvas_width: int,
    drawing_frequency: int,
) -> list[np.ndarray]:
    """
    Render every drawing_frequency-th state, as in HW1. Author/reviewer: TODO.

    Return RGB arrays of shape (canvas_width, canvas_width, 3) for imageio.
    Render saved snapshots without advancing or mutating the simulation.
    """

    images: list[np.ndarray] = []

    for i, environment in enumerate(time_points):
        if i % drawing_frequency == 0:
            frame = draw_to_canvas(environment, canvas_width)
            images.append(frame)

    return images


def draw_to_canvas(environment: Environment, canvas_width: int) -> np.ndarray:
    """
    Render a snapshot with an offscreen Pygame surface. Author/reviewer: TODO.

    Scale coordinates by canvas_width / environment.width. Return the RGB
    array with axes ordered (height, width, channels), matching HW1 output.
    """
    # Create a square canvas with a white background.
    surface = pygame.Surface((canvas_width, canvas_width))
    surface.fill((255, 255, 255))

    # Draw each bacterium in the environment.
    for bacterium in environment.bacteria:
        draw_bacterium(
            surface,
            bacterium,
            environment.width,
            canvas_width,
        )

    # Convert to NumPy array (swap axes for imageio compatibility)
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)



def draw_bacterium(
    surface: pygame.Surface,
    bacterium: Bacterium,
    environment_width: float,
    canvas_width: int,
) -> None:
    """
    Draw one living agent with its population's color. Author/reviewer: TODO.

    Corresponds to draw_boid in HW1. Start with circles for attackers and
    targets rather than bird triangles; drawing size is only a display choice.
    """

    # Choose color based on alive status and bacteria type.
    if not bacterium.alive:
        color = (150, 150, 150)  # Gray for dead bacteria
    elif bacterium.bacteria_type == "attacker":
        color = (255, 80, 80)    # Red for attackers
    else:
        color = (80, 200, 120)    # Green for targets

    # Convert environment coordinates to canvas coordinates.
    scale = canvas_width / environment_width
    x = round(bacterium.position.x * scale)
    y = round(bacterium.position.y * scale)

    radius = 4

    pygame.draw.circle(surface, color, (x, y), radius)
