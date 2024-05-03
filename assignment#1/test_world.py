import constants
from creature import Creature
from world import World


def test_create_creature() -> None:
    world = World()
    creature = world._create_creature(constants.PREDATOR)
    assert creature.name == constants.PREDATOR
    assert creature.health in constants.HEALTH_VALUES
    assert creature.stamina in constants.STAMINA_VALUES
    assert creature.legs in constants.LEGS_VALUES
    assert creature.wings in constants.WINGS_VALUES
    assert creature.claws in constants.CLAWS_VALUES
    assert creature.teeth in constants.TEETH_VALUES
    assert creature.coordinate in constants.COORDINATE_VALUES


def test_simulate_interaction() -> None:
    world = World()
    world.simulate_interaction()
    assert world.predator is not None
    assert world.pray is not None


def test_fight_predator_wins() -> None:
    predator = Creature(
        constants.PREDATOR,
        100,
        80,
        5,
        4,
        2,
        constants.BIG_CLAWS,
        constants.SHARP_TEETH,
        0,
    )
    pray = Creature(
        constants.PRAY, 50, 60, 2, 2, 0, constants.SMALL_CLAWS, constants.SHARP_TEETH, 0
    )

    assert predator.power == 32
    assert pray.power == 10

    World._fight(predator, pray)
    assert predator.health == 90
    assert pray.health < 0


def test_fight_pray_wins() -> None:
    predator = Creature(
        constants.PREDATOR,
        50,
        80,
        2,
        4,
        2,
        constants.SMALL_CLAWS,
        constants.SHARP_TEETH,
        0,
    )
    pray = Creature(
        constants.PRAY, 100, 60, 5, 2, 0, constants.BIG_CLAWS, constants.SHARP_TEETH, 0
    )

    assert predator.power == 10
    assert pray.power == 32

    World._fight(predator, pray)
    assert predator.health < 0
    assert pray.health == 80
