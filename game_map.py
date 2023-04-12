import enum
import random

import pygame
import consts


def vec2Real(v: pygame.Vector2) -> pygame.Vector2:
    return v*consts.tile_size + pygame.Vector2(consts.x_offset, consts.y_offset)


class Tiles(enum.Enum):
    Grass = 1
    Road = 2
    TowerSpot = 3


class Direction(enum.Enum):
    Up = 1,
    Right = 2,
    Down = 3,


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.map = [[Tiles.Grass for x in range(
            self.width)] for y in range(height)]
        self.path = list[pygame.Vector2]

    def draw(self, screen: pygame.Surface):
        for y in range(0, consts.tile_height):
            for x in range(0, consts.tile_width):
                tile = self.map[y][x]
                p = pygame.Vector2(x, y)*consts.tile_size + \
                    pygame.Vector2(consts.x_offset, consts.y_offset)

                color = consts.CLR_GRASS if tile == Tiles.Grass else consts.CLR_ROAD
                pygame.draw.rect(screen, color,
                                 (p.x, p.y, consts.tile_size, consts.tile_size))

        for (x,y) in self.path:
            pygame.draw.circle(
                screen, (200, 50, 50), (x,y), 2)

    def generate_path(self):
        self.map = [[Tiles.Grass for x in range(
            self.width)] for y in range(self.height)]
        self.path = []

        x = 0
        y = random.randrange(int(self.height/3), int(self.height*2/3))
        self.map[y][x] = Tiles.Road
        x = 1
        prev_x = 0
        prev_y = y
        prev_dir = Direction.Right

        self.path.append(pygame.Vector2(0, y))

        while (x < self.width-1):
            self.map[y][x] = Tiles.Road

            chances = []
            go_up_chance = 0 if (
                prev_y < y or y <= 2 or self.map[y-1][x-1] == Tiles.Road) else 50
            for _ in range(0, go_up_chance):
                chances.append(Direction.Up)

            go_down_chance = 0 if prev_y > y or y >= self.height - \
                2 or self.map[y+1][x-1] == Tiles.Road else 50
            for _ in range(0, go_down_chance):
                chances.append(Direction.Down)

            go_right_chance = 100-(go_down_chance+go_up_chance)
            for _ in range(0, go_right_chance):
                chances.append(Direction.Right)

            random.shuffle(chances)
            choice = chances[0]
            if prev_dir != choice:
                self.path.append(pygame.Vector2(x, y))
            prev_x = x
            prev_y = y
            if choice == Direction.Up:
                y -= 1
            elif choice == Direction.Right:
                x += 1
            elif choice == Direction.Down:
                y += 1
                
            prev_dir = choice

        self.path.append(pygame.Vector2(self.width-1,y))
        h = consts.tile_size/2
        for i in range(len(self.path)):
            self.path[i] = vec2Real(self.path[i])+pygame.Vector2(h, h)
        self.map[y][self.width-1] = Tiles.Road
