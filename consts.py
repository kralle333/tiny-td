from pygame import Surface, Vector2
import pygame

game_width = 640
game_height = 480
tile_size = 64
y_offset = tile_size/2
x_offset = 0
tile_width = int(game_width/tile_size)
tile_height = int((game_height-y_offset)/tile_size)


def rect_in_bounds(p: Vector2, size: Vector2):
    pass


def circle_in_bounds(p: Vector2, radius: float):
    return p.x > radius and p.y > (y_offset+radius) and p.x < game_width-radius and p.y < game_height-radius


def pct_to_rect(start_x: float, start_y: float, end_x: float, end_y: float) -> tuple[int, int, int, int]:
    x = start_x*game_width
    y = start_y*game_height
    w = (end_x*game_width)-x
    h = (end_y*game_height) - y

    return (x, y, w, h)


def draw_window(screen: Surface, rect: tuple[int, int, int, int], color: tuple[int, int, int], border_color: tuple[int, int, int], border_size: int):
    x, y, w, h = rect
    inner_rect = (x+border_size, y+border_size,
                  w-2*border_size, h-2*border_size)
    pygame.draw.rect(screen, border_color, rect)
    pygame.draw.rect(screen, color, inner_rect)


def get_color_variation(color: tuple[int, int, int], mul: float):
    r, g, b = color
    return (r*mul, g*mul, b*mul)

CLR_ENEMY = (130, 89, 174)
CLR_GRASS = (142, 191, 123)
CLR_ROAD = (244, 253, 171)
CLR_WINDOW = (200,200,200)
CLR_WINDOW_BORDER = (100,100,100)
