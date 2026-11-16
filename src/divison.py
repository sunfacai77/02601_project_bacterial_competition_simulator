from .bacterium import Bacterium
from .datatypes import OrderedPair

import random

MIN_DIVISION_INTEGRITY = 0.2

#bacteria compete for energy
ENERGY_COMPETE = 0.05
#attacker may not immediately divide when they reach growth threhold
DIVISION_DELAY = 0.2
#division will be inhibited by recently dead bacteria nearby
DEAD_EFFECT = 0.05

def update_energy(b: Bacterium, time_step: float, competitor: int) -> None:
    """Update a bacterium's energy and growth progress for one time step.

    First, replenish the bacterium's available energy.
    Then spend some of that energy on growth and add the amount spent to growth_stage,
    which tracks the total energy invested in growth since the last division.
    """
    #下一步：attacker和target会不会有不同的生长模式

    #add new energy to bacteria, negatively correlated with density
    base_energy_intake = b.energy_recovery_rate*time_step
    adjusted_energy_intake = base_energy_intake / (1.0 + ENERGY_COMPETE * competitor)

    b.energy = b.energy + adjusted_energy_intake


    #bacteria use energy to grow, the consumed energy is recorded in grow stage
    consumed_engery_growth = b.growth_rate * time_step * (1 + random.uniform(-0.1, 0.1)) #random consumption 90%~110%
    #下一步：need further implementation for consumption related with energy level?

    if b.energy > consumed_engery_growth:
        b.energy = b.energy - consumed_engery_growth
        b.growth_stage = b.growth_stage + consumed_engery_growth

def update_divide_state(b: Bacterium, time_step: float, dead_neighbour: int) -> None:
    """Advance a bacterium's division state by one time step.

    If the bacterium is not dividing, check whether its accumulated energy
    investment in growth has reached the growth threshold. If it has, mark
    the bacterium as dividing and start its division timer.

    If the bacterium is already dividing, advance its timer by time_step.
    Cells below the integrity threshold cannot start or continue division.

    """
    if b.integrity < MIN_DIVISION_INTEGRITY:
        b.is_division = False
        return

    if not b.is_division:
        if b.growth_stage >= b.growth_threshold:  #when bacteria grow enough, start dividing

            if b.bacteria_type == "attacker":
                state = random.random()

                inhibition = DEAD_EFFECT * dead_neighbour
                delay_probability = (DIVISION_DELAY + inhibition) / (1 + inhibition)

                if state < delay_probability:  # X percent of attackers delay their division for more attacks
                    return

            b.is_division = True

    else:
        b.division_time = b.division_time - time_step  #count for dividing preparation process

            
def divide(b: Bacterium, environment_width: float) -> Bacterium:
    """Update the parent in place and return a new daughter bacterium.

    Reset the parent's growth_stage to zero and clear its dividing state.
    Create a daughter of the same type at a nearby position with zero
    growth progress. The caller adds the returned daughter to the
    environment after the current time step's updates are complete.

    Raises ValueError before changing the parent if integrity is below 0.2.
    """
    if b.integrity < MIN_DIVISION_INTEGRITY:
        raise ValueError("Cell integrity must be at least 0.2 to divide.")

    b.growth_stage = 0.0
    b.division_time = 2.0
    b.is_division = False

    offset = 4 #same as the radius, the new born keep close with the parent

    if b.position.x > environment_width / 2: #ensure the new_born is in field
        offset = -offset

    return Bacterium(
        position=OrderedPair(b.position.x + offset, b.position.y),
        orientation=b.orientation,
        bacteria_type=b.bacteria_type,
        integrity=b.integrity,  # Inherit damage; division does not restore integrity.
        alive=True,
        attack_cooldown_remaining=b.attack_cooldown_remaining,
        energy=0.0,
        energy_recovery_rate=b.energy_recovery_rate,
        growth_rate=b.growth_rate,
        growth_stage=0.0,
        growth_threshold=b.growth_threshold,
        division_time=b.division_time,
        is_division=False,
    )  #return a new bacteria same as the parent



