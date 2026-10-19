from .bacterium import Bacterium
from .environment import Environment


ContactPair = tuple[Bacterium, Bacterium]


def detect_contacts(environment: Environment) -> list[ContactPair]:
    """
    Return unique living pairs within the threshold. Author/reviewer: TODO.

    Use distance(b0.position, b1.position) <= environment.contact_distance.
    distance is the OrderedPair helper in bacterium.py, matching HW1.
    Exclude self-pairs and do not return both (a, b) and (b, a).
    Like HW1 neighbor distances, this is ordinary Euclidean distance after
    wrap-around, not a minimum-image distance across opposite edges.
    """
    raise NotImplementedError("Implement contact detection.")


def kill_target(attacker: Bacterium, target: Bacterium) -> None:
    """
    Mark a living target dead after attacker contact. Author/reviewer: TODO.

    Only living attacker-target inputs may trigger killing. Contact has already
    been checked by the caller; same-type pairs must not trigger killing.
    """
    raise NotImplementedError("Implement the initial killing rule.")


def resolve_killing(contacts: list[ContactPair]) -> None:
    """
    Apply killing to eligible pairs in either order. Author/reviewer: TODO.

    Pairs must refer to agents in the new environment, so killing cannot
    change any earlier snapshot in time_points.
    """
    raise NotImplementedError("Implement contact resolution.")
