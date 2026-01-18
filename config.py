# config.py
import pygame

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Game settings
FPS = 60
STARTING_MONEY = 100
STARTING_LIVES = 20
TOWER_COSTS = {
    'basic': 50,
    'sniper': 100,
    'splash': 150,
    'slow': 120
}

# Tower stats
TOWER_STATS = {
    'basic': {'damage': 10, 'range': 100, 'fire_rate': 1000, 'color': BLUE},
    'sniper': {'damage': 30, 'range': 200, 'fire_rate': 2000, 'color': PURPLE},
    'splash': {'damage': 15, 'range': 80, 'fire_rate': 800, 'color': ORANGE, 'splash_radius': 40},
    'slow': {'damage': 5, 'range': 90, 'fire_rate': 500, 'color': GREEN, 'slow_factor': 0.5}
}