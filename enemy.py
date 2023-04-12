import random
import pygame
import consts
from pygame import Surface, Vector2


def rand_offset(n: Vector2) -> Vector2:
    offset = consts.tile_size/2
    return n + Vector2(random.uniform(-offset, offset), random.uniform(-offset, offset))


class Enemy:
    def __init__(self, path: list[Vector2]) -> None:
        x, y = path[0]
        self.color = consts.get_color_variation(
            consts.CLR_ENEMY, random.uniform(0.6, 1.2))
        self.pos = rand_offset(
            Vector2(x-consts.tile_size*random.randrange(1, 5), y))
        self.path = []
        self.radius = consts.tile_size/6
        self.min_radius = self.radius*0.8
        self.max_radius = self.radius*1.2
        self.increasing = True if random.randint(0, 1) == 1 else False
        self.radius_change_speed = random.uniform(0.1, 0.2)
        for p in path:
            self.path.append(rand_offset(p))
        self.speed = random.uniform(0.2, 2)
        self.path_index = 0
        self.stopped = False

    def update(self):
        self.update_radius()
        if self.stopped:
            self.pos += Vector2(self.speed, 0)
            return
        r = self.path[self.path_index]-self.pos
        if r.length() < self.speed:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.stopped = True
        else:
            dir = r.normalize()
            self.pos += dir*self.speed

    def update_radius(self):
        if self.radius >= self.max_radius:
            self.increasing = False
            self.radius = self.max_radius
            self.radius_change_speed = 0.08
        elif self.radius <= self.min_radius:
            self.increasing = True
            self.radius = self.min_radius
            self.radius_change_speed = 0.15
        val = self.radius_change_speed * (1 if self.increasing else -1)
        self.radius += val

    def draw(self, screen: Surface):
        if not consts.circle_in_bounds(self.pos, self.radius):
            return

        pygame.draw.circle(screen, self.color,
                           (self.pos.x, self.pos.y), self.radius)
