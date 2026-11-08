import random
import unittest
from unittest.mock import patch

from src.bacterium import Bacterium
from src.datatypes import OrderedPair
from src.divison import divide
from src.environment import update_environment
from src.initialization import initialize_environment
from src.interactions import resolve_killing


class AttackCooldownTests(unittest.TestCase):
    def contact_environment(self):
        environment = initialize_environment(
            1, 1, 100.0, 0.0, 0.0, 1.0, 1.0, 0.0, seed=7
        )
        for cell in environment.bacteria:
            cell.position = OrderedPair(50.0, 50.0)
            cell.growth_threshold = 1000000.0
        environment.bacteria[0].energy = 100.0
        return environment

    def test_one_attacker_cannot_hit_multiple_targets_or_spend_energy_while_cooling(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                attacker = Bacterium(bacteria_type="attacker", energy=8.0)
                first = Bacterium(bacteria_type="target")
                second = Bacterium(bacteria_type="target")
                contacts = [(attacker, first), (second, attacker)]
                if reverse:
                    contacts = [(b, a) for a, b in contacts]
                with patch("src.interactions.random.uniform", return_value=0.5) as damage:
                    resolve_killing(contacts)
                    resolve_killing(contacts)
                self.assertEqual((first.integrity, second.integrity), (0.5, 1.0))
                self.assertEqual(attacker.energy, 4.0)
                self.assertEqual(attacker.attack_cooldown_remaining, 5.0)
                self.assertEqual(damage.call_count, 1)

    def test_cooldown_expires_after_five_seconds_at_different_step_sizes(self):
        for time_step, steps in ((0.1, 50), (0.25, 20), (1.0, 5)):
            with self.subTest(time_step=time_step):
                environment = self.contact_environment()
                with patch("src.interactions.random.uniform", return_value=0.4) as damage:
                    environment = update_environment(environment, time_step, rng=random.Random(7))
                    self.assertEqual(damage.call_count, 1)
                    for _ in range(steps - 1):
                        environment = update_environment(environment, time_step, rng=random.Random(7))
                        self.assertEqual(damage.call_count, 1)
                    environment = update_environment(environment, time_step, rng=random.Random(7))
                    self.assertEqual(damage.call_count, 2)
                self.assertEqual(environment.bacteria[0].attack_cooldown_remaining, 5.0)

    def test_cooldown_advances_out_of_contact_and_during_division(self):
        for dividing in (False, True):
            with self.subTest(dividing=dividing):
                environment = self.contact_environment()
                attacker = environment.bacteria[0]
                attacker.attack_cooldown_remaining = 5.0
                attacker.is_division = dividing
                attacker.division_time = 20.0
                environment.bacteria[1].position = OrderedPair(80.0, 80.0)
                updated = update_environment(environment, 2.0, rng=random.Random(7))
                self.assertEqual(updated.bacteria[0].attack_cooldown_remaining, 3.0)
                self.assertEqual(updated.bacteria[1].integrity, 1.0)
                self.assertAlmostEqual(updated.bacteria[0].energy, 102.0)

    def test_failed_attack_does_not_start_cooldown(self):
        for energy, dividing, target_alive in ((3.9, False, True), (8.0, True, True), (8.0, False, False)):
            with self.subTest(energy=energy, dividing=dividing, target_alive=target_alive):
                attacker = Bacterium(bacteria_type="attacker", energy=energy, is_division=dividing)
                target = Bacterium(bacteria_type="target", alive=target_alive)
                resolve_killing([(attacker, target)])
                self.assertEqual(attacker.attack_cooldown_remaining, 0.0)
                self.assertEqual(attacker.energy, energy)

    def test_previous_snapshots_keep_their_cooldown_values(self):
        original = self.contact_environment()
        with patch("src.interactions.random.uniform", return_value=0.4):
            first = update_environment(original, 0.1, rng=random.Random(7))
            second = update_environment(first, 1.0, rng=random.Random(7))
        self.assertEqual(original.bacteria[0].attack_cooldown_remaining, 0.0)
        self.assertEqual(first.bacteria[0].attack_cooldown_remaining, 5.0)
        self.assertEqual(second.bacteria[0].attack_cooldown_remaining, 4.0)

    def test_division_does_not_reset_remaining_cooldown(self):
        parent = Bacterium(
            bacteria_type="attacker", attack_cooldown_remaining=3.0,
            position=OrderedPair(50.0, 50.0), growth_stage=8.0,
            is_division=True, division_time=0.0,
        )
        daughter = divide(parent, 100.0)
        self.assertEqual(parent.attack_cooldown_remaining, 3.0)
        self.assertEqual(daughter.attack_cooldown_remaining, 3.0)

    def test_nonpositive_time_steps_cannot_trigger_attacks(self):
        for time_step in (0.0, -0.1):
            with self.subTest(time_step=time_step):
                original = self.contact_environment()
                with self.assertRaises(ValueError):
                    update_environment(original, time_step)
                self.assertEqual(original.bacteria[0].energy, 100.0)
                self.assertEqual(original.bacteria[1].integrity, 1.0)


if __name__ == "__main__":
    unittest.main()
