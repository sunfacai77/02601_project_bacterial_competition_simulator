import random
import unittest
from unittest.mock import patch

from src.bacterium import Bacterium
from src.datatypes import OrderedPair
from src.divison import divide, update_divide_state
from src.environment import update_environment
from src.initialization import initialize_environment


class DivisionIntegrityTests(unittest.TestCase):
    def test_low_integrity_prevents_starting_and_continuing_division(self):
        for bacteria_type in ("attacker", "target"):
            for dividing in (False, True):
                with self.subTest(bacteria_type=bacteria_type, dividing=dividing):
                    cell = Bacterium(
                        bacteria_type=bacteria_type, integrity=0.19,
                        growth_stage=8.0, growth_threshold=8.0,
                        is_division=dividing, division_time=1.0,
                    )
                    update_divide_state(cell, 0.1)
                    self.assertFalse(cell.is_division)
                    self.assertEqual(cell.division_time, 1.0)
                    self.assertEqual(cell.growth_stage, 8.0)

    def test_direct_division_below_threshold_fails_without_changing_parent(self):
        cell = Bacterium(
            integrity=0.19, growth_stage=8.0, is_division=True, division_time=0.0
        )
        with self.assertRaises(ValueError):
            divide(cell, 100.0)
        self.assertEqual(cell.growth_stage, 8.0)
        self.assertTrue(cell.is_division)
        self.assertEqual(cell.division_time, 0.0)

    def test_environment_division_respects_the_exact_threshold(self):
        for bacteria_type in ("attacker", "target"):
            for integrity, expected_count in ((0.19, 1), (0.2, 2), (1.0, 2)):
                with self.subTest(bacteria_type=bacteria_type, integrity=integrity):
                    original = initialize_environment(
                        num_attackers=int(bacteria_type == "attacker"),
                        num_targets=int(bacteria_type == "target"), width=100.0,
                        max_bacterium_speed=0.0, proximity=0.0, contact_distance=0.0,
                        mean_run_time=1.0, motility_speed=0.0, seed=7,
                    )
                    cell = original.bacteria[0]
                    cell.integrity = integrity
                    cell.growth_stage = cell.growth_threshold
                    update_divide_state(cell, 0.1)
                    self.assertEqual(cell.is_division, integrity >= 0.2)
                    # Also exercise cells whose preparation timer already expired.
                    cell.is_division = True
                    cell.division_time = 0.0
                    updated = update_environment(original, 0.1, rng=random.Random(7))
                    self.assertEqual(len(updated.bacteria), expected_count)
                    self.assertTrue(all(b.integrity == integrity for b in updated.bacteria))
                    self.assertTrue(all(not b.is_division for b in updated.bacteria))
                    self.assertAlmostEqual(updated.bacteria[0].energy, 0.1)
                    self.assertEqual(len(original.bacteria), 1)

    def test_attack_during_preparation_prevents_later_division(self):
        environment = initialize_environment(
            num_attackers=1, num_targets=1, width=100.0,
            max_bacterium_speed=0.0, proximity=0.0, contact_distance=1.0,
            mean_run_time=1.0, motility_speed=0.0, seed=7,
        )
        attacker, target = environment.bacteria
        attacker.position = OrderedPair(50.0, 50.0)
        target.position = OrderedPair(50.0, 50.0)
        attacker.energy = 4.0
        target.integrity = 0.6
        target.growth_stage = target.growth_threshold
        target.is_division = True
        target.division_time = 1.0
        with patch("src.interactions.random.uniform", return_value=0.5):
            wounded = update_environment(environment, 0.1, rng=random.Random(7))
        self.assertTrue(wounded.bacteria[1].alive)
        self.assertLess(wounded.bacteria[1].integrity, 0.2)
        for _ in range(12):
            wounded = update_environment(wounded, 0.1, rng=random.Random(7))
        self.assertEqual(len(wounded.bacteria), 2)
        self.assertFalse(wounded.bacteria[1].is_division)
        self.assertTrue(wounded.bacteria[1].alive)


if __name__ == "__main__":
    unittest.main()
