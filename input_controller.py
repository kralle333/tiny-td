import pygame

from enum import Enum


class InputOption(Enum):
    Invalid = 0
    Accept = 1
    Cancel = 2
    Options = 3
    Start = 4
    Select = 5


class InputController:
    def __init__(self, mapping: dict[InputOption, int], alt_mapping: dict[InputOption, int] = None) -> None:
        self.mappings = mapping
        self.alt_mapping = alt_mapping
        self.keys = None
        self.prev_keys = None

    def set_keys(self):
        self.keys = pygame.key.get_pressed()

    def set_prev(self):
        self.prev_keys = self.keys

    def is_pressed(self, option: InputOption):
        return self.keys[self.mappings[option]] or (self.alt_mapping != None and self.keys[self.mappings[option]])

    def is_new_pressed(self, option: InputOption):
        new_pressed = self.keys[self.mappings[option]
                                ] and not self.prev_keys[self.mappings[option]]
        alt_new_pressed = self.alt_mapping != None and self.keys[self.alt_mapping[option]
                                                                 ] and not self.prev_keys[self.alt_mapping[option]]
        return new_pressed or alt_new_pressed
