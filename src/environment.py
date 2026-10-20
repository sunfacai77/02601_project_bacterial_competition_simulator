from dataclasses import dataclass, field

from .bacterium import Bacterium, update_orientation, update_velocity, update_position
from .datatypes import OrderedPair



@dataclass
class Environment:
    """
    A square surface containing the bacteria at a single time point.

    Attributes:
        width: Side length of the square, following Sky.width / Universe.width.
        bacteria: Living and dead agents in this snapshot.
        max_bacterium_speed: Speed limit, corresponding to max_boid_speed.
        proximity: Neighborhood distance for future movement rules, as in HW1.
        contact_distance: Separate threshold for bacterial contact and killing.

    Defaults follow the zero/empty dataclass style of the homework. Set actual
    simulation parameters during initialization; they are not biological units.
    """

    width: float = 0.0
    bacteria: list[Bacterium] = field(default_factory=list)
    max_bacterium_speed: float = 0.0
    proximity: float = 0.0
    contact_distance: float = 0.0
    mean_run_time: float = 0.0
    motility_speed: float = 0.0

    def in_field(self, p: OrderedPair) -> bool:
        """
        Check [0, width] x [0, width], as in Universe.in_field. Author/reviewer: TODO.
        """

        if (0 <= p.x <= self.width) and (0 <= p.y <= self.width):
            return True
        else:
            return False

        # return (0 <= p.x <= self.width) and (0 <= p.y <= self.width)

def copy_environment(current_environment: Environment) -> Environment:
    """
    Return an independent copy, as in copy_sky/copy_universe. Author/reviewer: TODO.

    Copy every parameter and bacterium, including alive and bacteria_type.
    Allocate new OrderedPair objects for position, velocity, and acceleration.
    Mutating the copy must not change any previous time point.
    """
    # copy -> environment -> bacterium -> OrderedPair (3-layer DEEP COPY)

    new_environment = Environment(
        width=current_environment.width,
        max_bacterium_speed=current_environment.max_bacterium_speed,       #! 没有传bacterium，会通过defauly_factory=list自动创建一个空列表?
        proximity=current_environment.proximity,
        contact_distance=current_environment.contact_distance,
        mean_run_time=current_environment.mean_run_time,
        motility_speed=current_environment.motility_speed,
    )

    for bacterium in current_environment.bacteria:
        new_bacterium = Bacterium(
            position=OrderedPair(                                           #! 不能写position=bacterium.position, 是浅拷贝，后续会改改变原值
                bacterium.position.x,                                       #! 数值copy，对象不copy
                bacterium.position.y
            ),
            velocity=OrderedPair(
                bacterium.velocity.x, 
                bacterium.velocity.y
            ),

            orientation=bacterium.orientation,
            bacteria_type=bacterium.bacteria_type,
            health=bacterium.health,
            alive=bacterium.alive,

            energy=bacterium.energy,
            energy_recovery_rate=bacterium.energy_recovery_rate,

            growth_rate=bacterium.growth_rate,
            growth_stage=bacterium.growth_stage,
            growth_threshold=bacterium.growth_threshold,

            is_division=bacterium.is_division,
            division_time=bacterium.division_time,

            radius=bacterium.radius,
)


        new_environment.bacteria.append(new_bacterium)

    return new_environment


def update_environment(
    current_environment: Environment,
    time_step: float,
    rng = None,
) -> Environment:
    """
    Return the next snapshot, as in update_sky/update_universe. Author/reviewer: TODO.

    Copy the current environment first. For each living agent, preserve its old
    acceleration and velocity, compute acceleration from current_environment,
    then assign update_velocity and update_position results to the copied agent.
    After all motion is complete, detect contacts and resolve killing on the copy.
    Dead agents remain stored and stationary. Never mutate current_environment.
    """
    from .interactions import detect_contacts, resolve_killing

    next_environment = copy_environment(current_environment)

    for bacterium in next_environment.bacteria:
        if not bacterium.alive:
            continue

        # Compute new orientation and velocity of 'i' based on current environment
        
        bacterium.orientation = update_orientation(
            bacterium,
            current_environment.mean_run_time,
            time_step,
            rng=rng,

        )

        bacterium.velocity = update_velocity(
            bacterium,
            current_environment.motility_speed,
            current_environment.max_bacterium_speed,
        )

        bacterium.position = update_position(
            bacterium,
            current_environment.width,
            time_step,
        )



    # After all motion update is complete, detect contacts and resolve killing on the copy(interaction)
    contacts = detect_contacts(next_environment)      #! return a list of ContactPairs, a tuple of two bacteria
    resolve_killing(contacts)                         #! update the alive status of bacteria(or the health index)


    return next_environment
