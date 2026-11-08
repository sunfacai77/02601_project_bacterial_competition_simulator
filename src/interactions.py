import random

from .bacterium import Bacterium, distance
from .environment import Environment


ContactPair = tuple[Bacterium, Bacterium]
# finding the bacterium pairs that would contact(compute the euclidean distance for each pair)

# rules:
# [alive attacker , alive target] --> reduce integrity I; kill when I <= 0

# Modeling assumption, not an experimentally calibrated toxin damage range!
MIN_INTEGRITY_DAMAGE = 0.4
MAX_INTEGRITY_DAMAGE = 0.6

# Temporary model setting in seconds; applies across all targets of an attacker.
ATTACK_COOLDOWN = 1.0


def detect_contacts(environment: Environment) -> list[ContactPair]:
    """
    Return unique living pairs within the threshold. Author/reviewer: TODO.

    Use distance(b0.position, b1.position) <= environment.contact_distance.
    distance is the OrderedPair helper in bacterium.py, matching HW1.
    Exclude self-pairs and do not return both (a, b) and (b, a).
    Like HW1 neighbor distances, this is ordinary Euclidean distance after
    wrap-around, not a minimum-image distance across opposite edges.
    """

    bacteria = environment.bacteria
    threshold_dis = environment.contact_distance
    contacts = []

    # ranging over all of the bacteria, computing the distance for each pair
    #  Out layer: start from i (len(bacteria))
    #  Inner layer: start from i+1

    for i in range(len(bacteria)):
        b0 = bacteria[i]

        if not b0.alive:
            continue

        for j in range(i+1, len(bacteria)):
            b1 = bacteria[j]

            if not b1.alive:
                continue

            if distance(b0.position, b1.position) <= threshold_dis:
                contacts.append((b0, b1))

    return contacts



def kill_target(attacker: Bacterium, target: Bacterium) -> None:
    """
    Reduce a living target's integrity I after a successful attacker contact.

    Only living attacker-target inputs may trigger killing. Contact has already
    been checked by the caller; same-type pairs must not trigger killing.
    Each hit subtracts a uniform 0.4-0.6 of full integrity (1.0), not a fraction
    of remaining integrity. The target dies only when integrity falls to <= 0.
    The caller checks attack energy, division state, and cooldown.
    """

    if not attacker.alive or not target.alive:
        return

    if attacker.bacteria_type != "attacker":
        return

    if target.bacteria_type != "target":
        return

    # (attacker, target) satisfy the order, status and type

    target.integrity -= random.uniform(MIN_INTEGRITY_DAMAGE, MAX_INTEGRITY_DAMAGE)
    if target.integrity <= 0:
        target.alive = False



def resolve_killing(contacts: list[ContactPair]) -> None:
    """
    Apply killing to eligible pairs in either order. Author/reviewer: TODO.

    Pairs must refer to agents in the new environment, so killing cannot
    change any earlier snapshot in time_points.
    Each successful attack starts a cooldown shared across all possible targets.
    """
    # (attacker, target)
    kill_cost = 4  #attacker use engery to kill

    for b0, b1 in contacts:
        # Earlier contacts in this round may already have killed the target!
        if not b0.alive or not b1.alive:
            continue

        if b0.bacteria_type == "attacker" and b1.bacteria_type == "target" and (not b0.is_division):
            if b0.energy >= kill_cost and b0.attack_cooldown_remaining <= 0:
                b0.energy = b0.energy - kill_cost
                kill_target(b0, b1)
                b0.attack_cooldown_remaining = ATTACK_COOLDOWN

        elif b0.bacteria_type == "target" and b1.bacteria_type == "attacker" and (not b1.is_division):
            if b1.energy >= kill_cost and b1.attack_cooldown_remaining <= 0:
                b1.energy = b1.energy - kill_cost
                kill_target(b1, b0)
                b1.attack_cooldown_remaining = ATTACK_COOLDOWN

