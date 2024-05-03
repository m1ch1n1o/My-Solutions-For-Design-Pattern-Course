import constants


class AttackStrategy:
    def __init__(self) -> None:
        pass

    def calculate_power(self, power: int, teeth: str, claws: str) -> int:
        raise NotImplementedError


class GreedyAttackStrategy(AttackStrategy):
    def calculate_power(self, power: int, teeth: str, claws: str) -> int:
        power = self._calculate_teeth_power(power, teeth)
        return self._calculate_claws_power(power, claws)

    @staticmethod
    def _calculate_teeth_power(power: int, teeth: str) -> int:
        teeth_boosts = {
            constants.SHARP_TEETH: 3,
            constants.SHARPER_TEETH: 6,
            constants.SHARPEST_TEETH: 9,
        }
        # The creature must have one type of the teeth
        return power + teeth_boosts[teeth]

    @staticmethod
    def _calculate_claws_power(power: int, claws: str) -> int:
        claw_multipliers = {
            constants.SMALL_CLAWS: 2,
            constants.MEDIUM_CLAWS: 3,
            constants.BIG_CLAWS: 4,
        }
        # The creature must have one type of the claws
        return power * claw_multipliers[claws]
