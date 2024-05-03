import random

import constants
from creature import Creature


class World:
    def __init__(self) -> None:
        self.pray: Creature | None = None
        self.predator: Creature | None = None

    @staticmethod
    def _create_creature(name: str) -> Creature:
        health = random.choice(constants.HEALTH_VALUES)
        stamina = random.choice(constants.STAMINA_VALUES)
        power = random.choice(constants.POWER_VALUES)
        legs = random.choice(constants.LEGS_VALUES)
        wings = random.choice(constants.WINGS_VALUES)
        claws = random.choice(constants.CLAWS_VALUES)
        teeth = random.choice(constants.TEETH_VALUES)
        coordinate = random.choice(constants.COORDINATE_VALUES)

        creature = Creature(
            name, health, stamina, power, legs, wings, claws, teeth, coordinate
        )
        return creature

    def simulate_interaction(self) -> None:
        self.predator = self._create_creature(constants.PREDATOR)
        self.pray = self._create_creature(constants.PRAY)

        self._chase(self.predator, self.pray)

    def _chase(self, predator: Creature, pray: Creature) -> None:
        while predator.coordinate < pray.coordinate:
            predator.move()
            if predator.stamina <= 0:
                print("Pray ran into infinity \n")
                break
            pray.move()

            if predator.coordinate >= pray.coordinate:
                self._fight(predator, pray)
                break

    @staticmethod
    def _fight(predator: Creature, pray: Creature) -> None:
        print("Fight phase:")
        while True:
            predator.attack(pray)
            if pray.health <= 0:
                print("Some R-rated things have happened \n")
                break
            pray.attack(predator)
            if predator.health <= 0:
                print("Pray ran into infinity \n")
                break
