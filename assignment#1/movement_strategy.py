from typing import Tuple

import constants


class MovementStrategy:
    def __init__(self) -> None:
        pass

    def ret_after_move(self, coordinate: int, stamina: int) -> Tuple[int, int]:
        raise NotImplementedError


class GreedyMovementStrategy(MovementStrategy):
    def ret_after_move(self, coordinate: int, stamina: int) -> Tuple[int, int]:
        move_info = {
            constants.CRAWL: (0, 1, 1),
            constants.HOP: (20, 2, 3),
            constants.WALK: (40, 2, 4),
            constants.RUN: (60, 4, 6),
            constants.FLY: (80, 4, 8),
        }

        fastest_move = None
        for move_type, (stamina_requirement, _, _) in move_info.items():
            if stamina >= stamina_requirement:
                fastest_move = move_type

        if fastest_move:
            stamina_requirement, stamina_cost, coordinate_increment = move_info[
                fastest_move
            ]
            coordinate += coordinate_increment
            stamina -= stamina_cost
        return coordinate, stamina
