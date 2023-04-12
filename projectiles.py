
from pygame import Surface, Vector2
import pygame

import consts
from enemy import Enemy


class Projectile:
    def __init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.dir = Vector2(0, 0)
        self.alive = False
        self.radius = consts.tile_size/16

    def fire(self, from_pos: Vector2, to_pos: Vector2, speed: Vector2):
        self.dir = (to_pos-from_pos).normalize()
        self.pos = Vector2(from_pos)
        self.speed = speed
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.pos += self.dir*self.speed
        if not consts.circle_in_bounds(self.pos,self.radius):
            self.alive = False

    def draw(self, screen: Surface):
        if not self.alive:
            return
        pygame.draw.circle(screen,(10,10,10),(self.pos.x,self.pos.y),self.radius)
        rsh = 10/2
        # pygame.draw.rect(screen,
        #                  (200, 200, 200),
        #                  (self.pos.x-rsh,
        #                   self.pos.y-rsh,
        #                   rsh*2,
        #                   rsh*2))


class Projectiles:
    def __init__(self):
        self.projectiles: list[Projectile] = []
        for _ in range(10):
            self.projectiles.append(Projectile())

    def fire_projectile(self, from_pos: Vector2, enemy: Enemy):
        for p in self.projectiles:
            if not p.alive:
                p.fire(from_pos, enemy.pos, 2)
                return

        new_p = Projectile()
        new_p.fire(from_pos, enemy.pos, 2)
        self.projectiles.append(new_p)

    def update(self):
        for p in self.projectiles:
            p.update()

    def draw(self, screen: Surface):
        for p in self.projectiles:
            p.draw(screen)
