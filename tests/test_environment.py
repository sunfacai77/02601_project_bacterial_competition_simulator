import unittest
from unittest.mock import patch

from src.bacterium import Bacterium
from src.datatypes import OrderedPair
from src.environment import update_environment
from src.initialization import initialize_environment
from src.simulation import simulate_bacteria


class DeadCellClearanceTests(unittest.TestCase):
    def test_newly_killed_cell_is_cleared_ten_updates_after_death(self):
        environment = initialize_environment(
            1, 1, 100.0, 0.0, 0.0, 1.0, 1.0, 0.0, seed=7
        )
        attacker, target = environment.bacteria
        attacker.position = OrderedPair(50.0, 50.0)
        target.position = OrderedPair(50.0, 50.0)
        attacker.energy = 1.0
        target.integrity = 0.4

        with patch("src.interactions.random.uniform", return_value=0.5):
            snapshots = simulate_bacteria(environment, 11, 0.1)

        self.assertTrue(target.alive)
        for elapsed_steps, snapshot in enumerate(snapshots[1:11]):
            with self.subTest(elapsed_steps=elapsed_steps):
                dead_cell = snapshot.bacteria[1]
                self.assertFalse(dead_cell.alive)
                self.assertEqual(dead_cell.position, target.position)
                self.assertAlmostEqual(dead_cell.time_since_death, elapsed_steps * 0.1)
        self.assertEqual(len(snapshots[11].bacteria), 1)
        self.assertTrue(snapshots[11].bacteria[0].alive)

    def test_initial_dead_neighbor_stops_inhibiting_division_at_clearance(self):
        environment = initialize_environment(
            1, 0, 100.0, 0.0, 0.0, 1.0, 1.0, 0.0, seed=7,
            dead_cell_clearance_time=0.6,
        )
        attacker = environment.bacteria[0]
        dead_cell = Bacterium(position=attacker.position, alive=False)
        environment.bacteria.insert(0, dead_cell)

        with patch("src.environment.update_divide_state") as update_division:
            before_clearance = update_environment(environment, 0.25)
            after_clearance = update_environment(before_clearance, 0.4)

        self.assertEqual([call.args[2] for call in update_division.call_args_list], [1, 0])
        self.assertEqual(dead_cell.time_since_death, 0.0)
        self.assertEqual(before_clearance.bacteria[0].time_since_death, 0.25)
        self.assertEqual(after_clearance.dead_cell_clearance_time, 0.6)
        self.assertEqual(len(after_clearance.bacteria), 1)
        self.assertEqual(after_clearance.bacteria[0].position, attacker.position)
        self.assertTrue(after_clearance.bacteria[0].alive)
