import random
import unittest
from unittest.mock import patch

from src.bacterium import Bacterium, update_velocity
from src.datatypes import OrderedPair
from src.divison import divide
from src.environment import update_environment
from src.initialization import initialize_environment
from src.interactions import kill_target, resolve_killing


class IntegrityAttackTests(unittest.TestCase):
    def test_damage_accumulates_and_zero_integrity_is_lethal(self):
        attacker = Bacterium(bacteria_type="attacker")
        target = Bacterium(bacteria_type="target")
        with patch("src.interactions.random.uniform", return_value=0.5):
            kill_target(attacker, target)
            self.assertEqual(target.integrity, 0.5)
            self.assertTrue(target.alive)
            kill_target(attacker, target)
        self.assertEqual(target.integrity, 0.0)
        self.assertFalse(target.alive)

    def test_low_damage_requires_three_hits_and_negative_integrity_is_lethal(self):
        attacker = Bacterium(bacteria_type="attacker")
        target = Bacterium(bacteria_type="target")
        with patch("src.interactions.random.uniform", return_value=0.4):
            for _ in range(2):
                kill_target(attacker, target)
                self.assertTrue(target.alive)
            kill_target(attacker, target)
        self.assertLess(target.integrity, 0)
        self.assertFalse(target.alive)

    def test_random_hits_vary_within_the_damage_range(self):
        attacker = Bacterium(bacteria_type="attacker")
        damages = []
        generator = random.Random(7)
        with patch("src.interactions.random.uniform", side_effect=generator.uniform):
            for _ in range(20):
                target = Bacterium(bacteria_type="target")
                kill_target(attacker, target)
                damages.append(1.0 - target.integrity)
                self.assertTrue(target.alive)
        self.assertTrue(all(0.4 <= damage <= 0.6 for damage in damages))
        self.assertGreater(len(set(damages)), 1)

    def test_invalid_or_dead_pairs_do_not_attack_or_spend_energy(self):
        cases = [
            ("attacker", "attacker", True, True),
            ("target", "target", True, True),
            ("attacker", "target", False, True),
            ("attacker", "target", True, False),
        ]
        for first_type, second_type, first_alive, second_alive in cases:
            with self.subTest(pair=(first_type, second_type, first_alive, second_alive)):
                first = Bacterium(bacteria_type=first_type, alive=first_alive, energy=8.0)
                second = Bacterium(bacteria_type=second_type, alive=second_alive, energy=8.0)
                with patch("src.interactions.random.uniform") as damage:
                    kill_target(first, second)
                    resolve_killing([(first, second)])
                    damage.assert_not_called()
                self.assertEqual((first.integrity, second.integrity), (1.0, 1.0))
                self.assertEqual((first.energy, second.energy), (8.0, 8.0))

    def test_attack_cost_and_pair_order_are_preserved(self):
        for reversed_pair in (False, True):
            with self.subTest(reversed_pair=reversed_pair):
                attacker = Bacterium(bacteria_type="attacker", energy=4.0)
                target = Bacterium(bacteria_type="target")
                pair = (target, attacker) if reversed_pair else (attacker, target)
                with patch("src.interactions.random.uniform", return_value=0.5):
                    resolve_killing([pair])
                self.assertEqual(attacker.energy, 0.0)
                self.assertEqual(target.integrity, 0.5)
                self.assertTrue(target.alive)

    def test_dividing_or_underfunded_attackers_cannot_attack(self):
        for reversed_pair in (False, True):
            for energy, dividing in ((3.9, False), (8.0, True)):
                with self.subTest(energy=energy, dividing=dividing, reversed_pair=reversed_pair):
                    attacker = Bacterium(
                        bacteria_type="attacker", energy=energy, is_division=dividing
                    )
                    target = Bacterium(bacteria_type="target")
                    pair = (target, attacker) if reversed_pair else (attacker, target)
                    with patch("src.interactions.random.uniform") as damage:
                        resolve_killing([pair])
                        damage.assert_not_called()
                    self.assertEqual(attacker.energy, energy)
                    self.assertEqual(target.integrity, 1.0)

    def test_later_attackers_do_not_spend_energy_on_a_target_killed_this_round(self):
        attackers = [Bacterium(bacteria_type="attacker", energy=4.0) for _ in range(3)]
        target = Bacterium(bacteria_type="target")
        contacts = [(attackers[0], target), (target, attackers[1]), (attackers[2], target)]
        with patch("src.interactions.random.uniform", return_value=0.5) as damage:
            resolve_killing(contacts)
        self.assertFalse(target.alive)
        self.assertEqual(target.integrity, 0.0)
        self.assertEqual([attacker.energy for attacker in attackers], [0.0, 0.0, 4.0])
        self.assertEqual(damage.call_count, 2)

    def test_environment_updates_preserve_old_integrity_snapshots(self):
        original = initialize_environment(
            num_attackers=1, num_targets=1, width=100.0,
            max_bacterium_speed=2.0, proximity=0.0, contact_distance=1.0,
            mean_run_time=1.0, motility_speed=0.0, seed=7,
        )
        for bacterium in original.bacteria:
            self.assertEqual(bacterium.integrity, 1.0)
            bacterium.position = OrderedPair(50.0, 50.0)
        original.bacteria[0].energy = 4.0
        with patch("src.interactions.random.uniform", return_value=0.5):
            updated = update_environment(original, 0.1, rng=random.Random(7))
        self.assertEqual(original.bacteria[1].integrity, 1.0)
        self.assertEqual(updated.bacteria[1].integrity, 0.5)
        self.assertTrue(updated.bacteria[1].alive)
        self.assertIsNot(original.bacteria[1], updated.bacteria[1])
        self.assertEqual(original.bacteria[0].energy, 4.0)
        self.assertAlmostEqual(updated.bacteria[0].energy, 0.1)
        self.assertAlmostEqual(updated.bacteria[1].growth_stage, 0.1)

    def test_division_inherits_damage_without_healing_the_parent(self):
        parent = Bacterium(
            bacteria_type="target", position=OrderedPair(50.0, 50.0),
            integrity=0.35, energy=6.0, energy_recovery_rate=2.0,
            growth_rate=1.0, growth_stage=8.0, growth_threshold=8.0,
            is_division=True, division_time=0.0,
        )
        daughter = divide(parent, 100.0)
        self.assertEqual(parent.integrity, 0.35)
        self.assertEqual(daughter.integrity, 0.35)
        self.assertTrue(parent.alive and daughter.alive)
        self.assertEqual(parent.energy, 6.0)
        self.assertEqual(daughter.energy, 0.0)
        self.assertEqual(parent.growth_stage, 0.0)
        self.assertEqual(daughter.growth_stage, 0.0)

    def test_wounded_targets_keep_normal_movement_until_death(self):
        target = Bacterium(bacteria_type="target", integrity=0.2, orientation=0.0)
        moving = update_velocity(target, motility_speed=2.0, max_bacterium_speed=2.0)
        self.assertEqual((moving.x, moving.y), (2.0, 0.0))
        target.integrity = 0.0
        target.alive = False
        stopped = update_velocity(target, motility_speed=2.0, max_bacterium_speed=2.0)
        self.assertEqual((stopped.x, stopped.y), (0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
