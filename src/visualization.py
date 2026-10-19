from __future__ import annotations

from typing import TYPE_CHECKING

from .bacterium import Bacterium
from .environment import Environment

if TYPE_CHECKING:
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
    raise NotImplementedError("Implement snapshot animation.")


def draw_to_canvas(environment: Environment, canvas_width: int) -> np.ndarray:
    """
    Render a snapshot with an offscreen Pygame surface. Author/reviewer: TODO.

    Scale coordinates by canvas_width / environment.width. Return the RGB
    array with axes ordered (height, width, channels), matching HW1 output.
    """
    raise NotImplementedError("Implement a single frame.")


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
    raise NotImplementedError("Implement bacterium drawing.")
