from ctypes import Union
from typing import Sequence, Tuple
from pygame import Color, Surface, Vector2
import pygame
from enemy import Enemy
from projectiles import Projectiles
import consts


class TowerConfig:
    def __init__(self, cooldown_per_shot: int, target_dist: float, color: Tuple[int, int, int]) -> None:
        self.cooldown_per_shot = cooldown_per_shot
        self.target_dist = target_dist
        self.color = color


def red_tower_cfg() -> TowerConfig:
    return TowerConfig(1000, 100, (220, 133, 128))


def green_tower_cfg() -> TowerConfig:
    return TowerConfig(1000, 100, (149, 218, 182))


def yellow_tower_cfg() -> TowerConfig:
    return TowerConfig(1000, 100, (242, 230, 177))


class Tower:
    def __init__(self, pos: Vector2, cfg: TowerConfig):
        self.pos = pos
        self.cfg = cfg
        self.cool_down = cfg.cooldown_per_shot

    def update(self, delta_time: int, projectiles: Projectiles, enemies: list[Enemy]):
        if self.cool_down > 0:
            self.cool_down -= delta_time
            return
        self.cool_down = self.cfg.cooldown_per_shot
        closest = None
        closest_dist = 1000000
        for e in enemies:
            this_dist = (self.pos-e.pos).length()
            if this_dist < closest_dist:
                closest = e
                closest_dist = this_dist

        if closest == None or closest_dist > self.cfg.target_dist:
            return
        projectiles.fire_projectile(
            self.pos+Vector2(consts.tile_size/2,
                             consts.tile_size/2), closest)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen,
                         self.cfg.color,
                         (self.pos.x,
                          self.pos.y,
                          consts.tile_size,
                          consts.tile_size))
