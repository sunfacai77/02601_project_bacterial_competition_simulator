from .bacterium import Bacterium, distance
from .environment import Environment


ContactPair = tuple[Bacterium, Bacterium]
# finding the bacterium pairs that would contact(compute the euclidean distance for each pair)

# rules:
# [alive attacker , alive target] --> kill
# health change...? density...?  division speed?



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
    Mark a living target dead after attacker contact. Author/reviewer: TODO.

    Only living attacker-target inputs may trigger killing. Contact has already
    been checked by the caller; same-type pairs must not trigger killing.
    """

    # if attacker & target --> target.alive = False

    if not attacker.alive or not target.alive:
        return

    if attacker.bacteria_type != "attacker":
        return

    if target.bacteria_type != "target":
        return

    # (attacker, target) satisfy the order, status and type

    target.alive = False



def resolve_killing(contacts: list[ContactPair]) -> None:
    """
    Apply killing to eligible pairs in either order. Author/reviewer: TODO.

    Pairs must refer to agents in the new environment, so killing cannot
    change any earlier snapshot in time_points.
    """
    # (attacker, target)
    for b0, b1 in contacts:
        if b0.bacteria_type == "attacker" and b1.bacteria_type == "target":
            kill_target(b0, b1)

        elif b0.bacteria_type == "target" and b1.bacteria_type == "attacker":
            kill_target(b1, b0)
