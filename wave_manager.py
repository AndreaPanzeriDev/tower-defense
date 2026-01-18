# wave_manager.py
import pygame
import random
from config import *
from enemies import Enemy

class WaveManager:
    def __init__(self):
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_in_wave = 10
        self.spawn_timer = 0
        self.spawn_delay = 60  # Frames between spawns
        self.wave_active = False
        self.wave_complete = False
        
    def start_wave(self):
        self.wave_active = True
        self.wave_complete = False
        self.enemies_spawned = 0
        self.enemies_in_wave = 5 + self.wave * 2
    
    def update(self, enemies, path):
        if not self.wave_active:
            return
        
        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay and self.enemies_spawned < self.enemies_in_wave:
            self.spawn_timer = 0
            self.enemies_spawned += 1
            
            # Determine enemy type based on wave
            enemy_type = "normal"
            health = 20 + (self.wave * 5)
            speed = 2
            bounty = 5 + self.wave
            
            if self.wave > 3 and random.random() < 0.3:
                enemy_type = "fast"
                speed = 4
                health = int(health * 0.7)
                bounty = bounty + 2
            
            if self.wave > 5 and random.random() < 0.2:
                enemy_type = "tank"
                speed = 1.5
                health = int(health * 2)
                bounty = bounty + 5
            
            enemy = Enemy(path[0][0], path[0][1], health, speed, bounty, enemy_type)
            enemy.set_path(path)
            enemies.append(enemy)
        
        # Check wave complete
        if (self.enemies_spawned >= self.enemies_in_wave and 
            not any(e.alive for e in enemies)):
            self.wave_active = False
            self.wave_complete = True
            self.wave += 1
    
    def get_current_wave(self):
        return self.wave
    
    def is_wave_active(self):
        return self.wave_active
    
    def is_wave_complete(self):
        return self.wave_complete
    
    def reset_wave_complete(self):
        self.wave_complete = False