from __future__ import annotations

import constants
from attack_strategy import AttackStrategy, GreedyAttackStrategy
from movement_strategy import GreedyMovementStrategy, MovementStrategy


class Creature:
    def __init__(
        self,
        name: str,
        health: int,
        stamina: int,
        power: int,
        legs: int,
        wings: int,
        claws: str,
        teeth: str,
        coordinate: int,
        movement_strategy: MovementStrategy = GreedyMovementStrategy(),
        attack_strategy: AttackStrategy = GreedyAttackStrategy(),
    ) -> None:
        self.name = name
        self.health = health
        self.stamina = stamina
        self.power = power
        self.legs = legs
        self.wings = wings
        self.claws = claws
        self.teeth = teeth
        self.coordinate = 0 if name == constants.PREDATOR else coordinate
        self.movement_strategy = movement_strategy
        self.attack_strategy = attack_strategy

        self._update_skills()
        self._log_characteristics()

    def _update_skills(self) -> None:
        self._calculate_moving_skills()
        # use power calculation strategy
        self.power = self.attack_strategy.calculate_power(
            self.power, self.teeth, self.claws
        )

    def _calculate_moving_skills(self) -> None:
        self.move_skills = [constants.CRAWL]

        if self.legs >= 1:
            self.move_skills.append(constants.HOP)
        if self.legs >= 2:
            self.move_skills.extend([constants.WALK, constants.RUN])

        if self.wings >= 2:
            self.move_skills.append(constants.FLY)

    def _log_characteristics(self) -> None:
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Stamina: {self.stamina}")
        print(f"Power: {self.power}")
        print(f"Legs: {self.legs}")
        print(f"Wings: {self.wings}")
        print(f"Claws: {self.claws}")
        print(f"Teeth: {self.teeth}")
        print(f"Coordinate: {self.coordinate}")
        print("Move Skills:", ", ".join(self.move_skills))
        print()

    # Greedy algorithm
    def move(self) -> None:
        # Use the movement strategy
        coordinate, stamina = self.movement_strategy.ret_after_move(
            self.coordinate, self.stamina
        )
        self.coordinate = coordinate
        self.stamina = stamina

    def attack(self, creature: Creature) -> None:
        creature.health -= self.power
