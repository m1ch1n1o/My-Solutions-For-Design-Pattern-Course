import unittest

import constants
from attack_strategy import GreedyAttackStrategy
from creature import Creature
from movement_strategy import GreedyMovementStrategy, MovementStrategy


def test_creating_predator() -> None:
    creature = Creature(
        constants.PREDATOR,
        61,
        80,
        3,
        2,
        2,
        constants.BIG_CLAWS,
        constants.SHARP_TEETH,
        0,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )

    assert creature.name == constants.PREDATOR
    assert creature.health == 61
    assert creature.stamina == 80
    assert creature.power == (3 + 3) * 4  # 24
    assert creature.legs == 2
    assert creature.wings == 2
    assert creature.claws == constants.BIG_CLAWS
    assert creature.teeth == constants.SHARP_TEETH
    assert creature.coordinate == 0


def test_creating_pray() -> None:
    creature = Creature(
        constants.PRAY,
        67,
        55,
        1,
        1,
        1,
        constants.SMALL_CLAWS,
        constants.SHARPEST_TEETH,
        123,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )

    assert creature.name == constants.PRAY
    assert creature.health == 67
    assert creature.stamina == 55
    assert creature.power == (1 + 9) * 2  # 20
    assert creature.legs == 1
    assert creature.wings == 1
    assert creature.claws == constants.SMALL_CLAWS
    assert creature.teeth == constants.SHARPEST_TEETH
    assert creature.coordinate == 123


def test_attack() -> None:
    predator = Creature(
        constants.PREDATOR,
        100,
        80,
        2,
        4,
        2,
        constants.BIG_CLAWS,
        constants.SHARP_TEETH,
        0,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )
    assert predator.power == 20

    pray = Creature(
        constants.PRAY,
        60,
        70,
        1,
        2,
        0,
        constants.SMALL_CLAWS,
        constants.SHARP_TEETH,
        0,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )
    assert pray.power == 8

    predator.attack(pray)
    assert pray.health == 40

    pray.attack(predator)
    assert predator.health == 92


class TestMovementStrategies(unittest.TestCase):
    creature = Creature(
        constants.PREDATOR,
        20,
        10,
        2,
        1,
        2,
        constants.SMALL_CLAWS,
        constants.SHARP_TEETH,
        0,
        movement_strategy=MovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )

    def test_move_method_raises_not_implemented_error(self) -> None:
        strategy = MovementStrategy()

        # Use assertRaises to check if the move method raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            strategy.ret_after_move(
                self.creature.coordinate, self.creature.stamina
            )  # Pass a creature instance or None


def test_greedy_movement_strategy_high_stamina() -> None:
    creature = Creature(
        constants.PREDATOR,
        20,
        80,
        2,
        4,
        2,
        constants.SMALL_CLAWS,
        constants.SHARP_TEETH,
        0,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )

    # Test Fly
    creature.move()
    assert creature.stamina == 76
    assert creature.coordinate == 8

    # Test Run
    creature.stamina = 62
    creature.move()
    assert creature.stamina == 58
    assert creature.coordinate == 14


def test_greedy_movement_strategy_low_stamina() -> None:
    creature = Creature(
        constants.PRAY,
        50,
        45,
        2,
        4,
        0,
        constants.SMALL_CLAWS,
        constants.SHARP_TEETH,
        14,
        movement_strategy=GreedyMovementStrategy(),
        attack_strategy=GreedyAttackStrategy(),
    )

    # Test Walk
    creature.move()
    assert creature.stamina == 43
    assert creature.coordinate == 18

    # Test Hop
    creature.stamina = 20
    creature.move()
    assert creature.stamina == 18
    assert creature.coordinate == 21

    # Test Crawl
    creature.move()
    assert creature.stamina == 17
    assert creature.coordinate == 22


class TestNotImplementedError(unittest.TestCase):
    def test_move_method_raises_not_implemented_error(self) -> None:
        creature = Creature(
            constants.PREDATOR,
            20,
            10,
            2,
            1,
            2,
            constants.SMALL_CLAWS,
            constants.SHARP_TEETH,
            0,
            movement_strategy=MovementStrategy(),
            attack_strategy=GreedyAttackStrategy(),
        )

        # Use assertRaises to check if the move method raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            creature.move()

        # creature should the fastest way to move
