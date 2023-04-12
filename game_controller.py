
from enum import Enum

from pygame import Surface, Vector2
import pygame
from input_controller import InputController, InputOption
from projectiles import Projectiles
import tower
from tower import Tower
from enemy import Enemy
import game_map
import consts


class GamePhase(Enum):
    Invalid = 0
    SelectOption = 1
    OutsideWave = 2
    InWave = 3
    GameOver = 4


class State:
    def __init__(self, max_lives: int, start_phase: GamePhase) -> None:
        self.wave = 1
        self.lives = max_lives
        self.max_lives = max_lives
        self.prev_phase = GamePhase.Invalid
        self.current_phase = start_phase

    def set_phase(self, new_phase: GamePhase):
        self.prev_phase = self.current_phase
        self.current_phase = new_phase


class GameController:
    def __init__(self, max_lives: int) -> None:
        self.state = State(max_lives, GamePhase.SelectOption)
        self.enemies: list[Enemy] = []
        self.towers: list[Tower] = []
        self.projectiles = Projectiles()

    def get_state(self) -> State:
        return self.state

    def update(self, delta_time: int, key_state: InputController) -> None:
        phase = self.state.current_phase
        if phase == GamePhase.SelectOption:
            if key_state.is_new_pressed(InputOption.Start):
                self.start_level()
        elif phase == GamePhase.InWave:
            for e in self.enemies:
                e.update()
            for t in self.towers:
                t.update(delta_time, self.projectiles, self.enemies)
            self.projectiles.update()
            pass
        elif phase == GamePhase.OutsideWave:
            if key_state.is_new_pressed(InputOption.Start):
                self.start_wave()
            pass
        elif phase == GamePhase.GameOver:
            pass

    def draw(self, screen):
        phase = self.state.current_phase
        if phase == GamePhase.SelectOption:
            consts.draw_window(screen, consts.pct_to_rect(
                0.1, 0.2, 0.9, 0.8), consts.CLR_WINDOW, consts.CLR_WINDOW_BORDER, 10)
            return

        self.current_map.draw(screen)
        for e in self.enemies:
            e.draw(screen)
        for t in self.towers:
            t.draw(screen)
        self.projectiles.draw(screen)

    def start_level(self):
        self.state.set_phase(GamePhase.OutsideWave)
        self.current_map = game_map.GameMap(
            consts.tile_width,
            consts.tile_height)
        self.current_map.generate_path()

    def start_wave(self):
        self.state.set_phase(GamePhase.InWave)
        self.state.wave += 1
        for i in range(5000):
            self.enemies.append(Enemy(self.current_map.path))
