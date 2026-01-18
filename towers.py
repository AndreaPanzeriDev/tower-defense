# towers.py
import pygame
import math
import time
from config import *
from game_objects import Projectile

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.stats = TOWER_STATS[tower_type]
        self.last_shot = 0
        self.cooldown = self.stats['fire_rate']
        self.level = 1
        
        # Visuals
        self.selected = False
    
    def update(self, enemies, current_time, projectiles):
        if not enemies:
            return
        
        # Check cooldown
        if current_time - self.last_shot < self.cooldown:
            return
        
        # Find target
        target = self.find_target(enemies)
        
        if target:
            self.shoot(target, projectiles)
            self.last_shot = current_time
    
    def find_target(self, enemies):
        # Find enemy in range with highest health (or closest to end)
        best_target = None
        max_health = -1
        
        for enemy in enemies:
            if not enemy.alive:
                continue
            
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.stats['range']:
                # Prioritize enemies with more health
                if enemy.health > max_health:
                    max_health = enemy.health
                    best_target = enemy
        
        return best_target
    
    def shoot(self, target, projectiles):
        proj = Projectile(self.x, self.y, target, self.stats['damage'], self.tower_type)
        projectiles.append(proj)
    
    def draw(self, surface):
        # Draw range circle if selected
        if self.selected:
            pygame.draw.circle(surface, (100, 100, 100, 100), 
                             (int(self.x), int(self.y)), self.stats['range'], 1)
        
        # Draw tower base
        pygame.draw.rect(surface, (60, 60, 60), 
                        (self.x - 15, self.y - 15, 30, 30))
        
        # Draw tower top (color by type)
        color = self.stats['color']
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 12)
        
        # Draw level indicator
        level_color = YELLOW
        pygame.draw.circle(surface, level_color, (int(self.x + 8), int(self.y - 8)), 4)
        
        # Draw turret direction (visual feedback)
        pygame.draw.line(surface, WHITE, 
                        (int(self.x), int(self.y)), 
                        (int(self.x + 15), int(self.y)), 2)
    
    def upgrade(self):
        self.level += 1
        # Increase stats based on level
        self.stats['damage'] = int(self.stats['damage'] * 1.5)
        self.stats['range'] = int(self.stats['range'] * 1.1)
        self.cooldown = max(100, self.cooldown * 0.9)