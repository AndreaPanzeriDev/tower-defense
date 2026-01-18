# game_objects.py
import pygame
import math
from config import *

class Projectile:
    def __init__(self, x, y, target, damage, tower_type):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.tower_type = tower_type
        self.speed = 8
        self.active = True
        
        # Splash effect
        self.splash = False
        if tower_type == 'splash':
            self.splash = True
            self.splash_radius = TOWER_STATS['splash']['splash_radius']
        
        # Slow effect
        self.slow = False
        if tower_type == 'slow':
            self.slow = True
            self.slow_factor = TOWER_STATS['slow']['slow_factor']
    
    def update(self, enemies):
        if not self.target or not self.target.alive:
            self.active = False
            return
        
        # Move towards target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < self.speed:
            # Hit target
            if self.splash:
                # Splash damage
                for enemy in enemies:
                    enemy_dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                    if enemy_dist <= self.splash_radius:
                        enemy.take_damage(self.damage)
            else:
                self.target.take_damage(self.damage)
            
            if self.slow:
                self.target.apply_slow(self.slow_factor)
            
            self.active = False
        else:
            # Move
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def draw(self, surface):
        if self.active:
            color = TOWER_STATS[self.tower_type]['color']
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 4)
            
            # Draw trail for visual feedback
            if self.tower_type == 'sniper':
                pygame.draw.line(surface, color, (int(self.x - 5), int(self.y)), 
                               (int(self.x), int(self.y)), 2)