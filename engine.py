from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handler import EventHandler


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap,  player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_eemy_turn(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'{entity.name} пытается ходить, но у него нет ножек')

    def handle_event(self, events: Set[Iterable]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.handle_eemy_turn()
            self.update_fov()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()



