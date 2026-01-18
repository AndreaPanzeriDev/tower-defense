# enemies.py
import pygame
import math
from config import *

class Enemy:
    def __init__(self, x, y, health, speed, bounty, enemy_type="normal"):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = health
        self.speed = speed
        self.base_speed = speed
        self.bounty = bounty
        self.alive = True
        self.enemy_type = enemy_type
        
        # Pathfinding
        self.path_index = 0
        self.path = []
        
        # Effects
        self.slow_factor = 1.0
        self.slow_timer = 0
    
    def set_path(self, path):
        self.path = path
        if path:
            self.x, self.y = path[0]
    
    def update(self):
        if not self.alive:
            return
        
        # Update slow effect
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
        
        # Move along path
        if self.path and self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            
            if dist < 2:
                self.path_index += 1
                if self.path_index >= len(self.path):
                    self.alive = False
                    return "reached_end"
            else:
                speed = self.speed * self.slow_factor
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed
        
        return None
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return self.bounty
        return 0
    
    def apply_slow(self, slow_factor):
        self.slow_factor = slow_factor
        self.slow_timer = 60  # 1 second at 60 FPS
    
    def draw(self, surface):
        if not self.alive:
            return
        
        # Draw enemy
        color = RED
        if self.enemy_type == "fast":
            color = YELLOW
        elif self.enemy_type == "tank":
            color = PURPLE
        
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 12)
        
        # Health bar
        bar_width = 30
        bar_height = 4
        health_percent = self.health / self.max_health
        
        # Background
        pygame.draw.rect(surface, BLACK, (self.x - bar_width//2, self.y - 20, bar_width, bar_height))
        # Health
        health_color = (int(255 * (1 - health_percent)), int(255 * health_percent), 0)
        pygame.draw.rect(surface, health_color, 
                        (self.x - bar_width//2, self.y - 20, bar_width * health_percent, bar_height))
        
        # Slow effect indicator
        if self.slow_factor < 1:
            pygame.draw.circle(surface, GREEN, (int(self.x), int(self.y)), 15, 2)