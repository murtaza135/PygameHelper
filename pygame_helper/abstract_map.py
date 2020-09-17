import pygame
from pygame_helper.utilities import XYTuple, WHTuple
from abc import ABC, abstractmethod
import json


class AbstractMap(ABC):
    
    def __init__(self, game_mode, map_path, tile_geometry):
        self.game_mode = game_mode
        self.window = None
        self.tile_map = None
        self.tile_key_to_class_mapping = dict()
        self.tile_objects = pygame.sprite.Group()

        self.num_tiles = None
        self.tile_geometry = WHTuple(*tile_geometry)
        self.window_geometry = None

        self._load_tile_map(map_path)
        self._load_tile_keys_from_tile_map()
        self._calculate_window_geometry()
        self._create_window_from_geometry()
        self.generate_map()

        self.regenerate_map = self.generate_map

    def _load_tile_map(self, map_path):
        try:
            with open(map_path, "r", encoding="utf-8") as f:
                self.tile_map = json.load(f)
        except (FileNotFoundError, TypeError) as e:
            self.tile_map = None

    def _load_tile_keys_from_tile_map(self):
        if self.tile_map is not None:
            for row in self.tile_map:
                for tile in row:
                    self.tile_key_to_class_mapping[tile] = None

    def _calculate_window_geometry(self):
        if self.tile_map is not None:
            self.num_tiles = XYTuple(x=len(self.tile_map[0]), y=len(self.tile_map))
            self.window_geometry = WHTuple(
                self.tile_geometry.width * self.num_tiles.x,
                self.tile_geometry.height * self.num_tiles.y
            )
        else:
            self.num_tiles = None
            self.window_geometry = None

    def _create_window_from_geometry(self):
        if self.window_geometry is not None:
            self.window = pygame.Surface((self.window_geometry))
        else:
            self.window = None

    @abstractmethod
    def generate_map(self):
        pass

    def render(self, window):
        window.blit(pygame.transform.scale(self.window, window.get_size()), (0, 0))

    def draw_grid(self, colour=(138, 138, 134)):
        for x in range(0, self.window_geometry.width, self.tile_geometry.width):
            pygame.draw.line(self.window, colour, (x, 0), (x, self.window_geometry.height))
        for y in range(0, self.window_geometry.height, self.tile_geometry.height):
            pygame.draw.line(self.window, colour, (0, y), (self.window_geometry.width, y))

    def delete_all_tile_objects(self):
        for tile_object in self.tile_objects:
            tile_object.kill()