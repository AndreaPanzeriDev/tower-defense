# main.py
import pygame
import math
import sys
from config import *
from towers import Tower
from enemies import Enemy
from game_objects import Projectile
from wave_manager import WaveManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Game state
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.game_over = False
        self.paused = False
        
        # Game objects
        self.towers = []
        self.enemies = []
        self.projectiles = []
        
        # Wave system
        self.wave_manager = WaveManager()
        
        # Path (simple path for demo)
        self.path = self.generate_path()
        
        # Selection state
        self.selected_tower = None
        self.placing_tower = False
        self.tower_type = None
        
        # UI state
        self.current_menu = "main"  # main, shop, towers, stats
        
    def generate_path(self):
        """Generate a simple path for enemies to follow"""
        path = []
        # Start left middle
        start_x = 0
        start_y = SCREEN_HEIGHT // 2
        path.append((start_x, start_y))
        
        # Right
        path.append((200, start_y))
        # Up
        path.append((200, start_y - 150))
        # Right
        path.append((500, start_y - 150))
        # Down
        path.append((500, start_y + 150))
        # Right to end
        path.append((SCREEN_WIDTH, start_y + 150))
        
        return path
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.placing_tower:
                        self.placing_tower = False
                        self.selected_tower = None
                    elif self.selected_tower:
                        self.selected_tower.selected = False
                        self.selected_tower = None
                    else:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    if not self.wave_manager.is_wave_active():
                        self.wave_manager.start_wave()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)
                elif event.button == 3:  # Right click
                    self.handle_right_click(event.pos)
    
    def handle_click(self, pos):
        x, y = pos
        
        # Check if clicking on a tower
        for tower in self.towers:
            if math.hypot(tower.x - x, tower.y - y) < 20:
                if self.selected_tower:
                    self.selected_tower.selected = False
                self.selected_tower = tower
                tower.selected = True
                self.placing_tower = False
                return
        
        # Check if clicking on UI buttons
        if self.check_ui_click(x, y):
            return
        
        # Place tower if in placing mode
        if self.placing_tower:
            if self.can_place_tower(x, y):
                if self.money >= TOWER_COSTS[self.tower_type]:
                    self.towers.append(Tower(x, y, self.tower_type))
                    self.money -= TOWER_COSTS[self.tower_type]
                    self.placing_tower = False
                    self.tower_type = None
    
    def handle_right_click(self, pos):
        x, y = pos
        # Deselect tower
        if self.selected_tower:
            self.selected_tower.selected = False
            self.selected_tower = None
        self.placing_tower = False
    
    def check_ui_click(self, x, y):
        """Check if clicking on UI buttons"""
        button_width = 120
        button_height = 40
        start_y = SCREEN_HEIGHT - 100
        
        # Tower buttons
        tower_types = ['basic', 'sniper', 'splash', 'slow']
        for i, t_type in enumerate(tower_types):
            btn_x = 20 + i * (button_width + 10)
            if (btn_x <= x <= btn_x + button_width and 
                start_y <= y <= start_y + button_height):
                if self.money >= TOWER_COSTS[t_type]:
                    self.placing_tower = True
                    self.tower_type = t_type
                    if self.selected_tower:
                        self.selected_tower.selected = False
                        self.selected_tower = None
                    return True
        
        # Start wave button
        start_btn_x = SCREEN_WIDTH - 140
        start_btn_y = SCREEN_HEIGHT - 100
        if (start_btn_x <= x <= start_btn_x + 120 and 
            start_btn_y <= y <= start_btn_y + 40):
            if not self.wave_manager.is_wave_active():
                self.wave_manager.start_wave()
                return True
        
        # Upgrade button (when tower selected)
        if self.selected_tower:
            upgrade_btn_x = SCREEN_WIDTH - 140
            upgrade_btn_y = SCREEN_HEIGHT - 60
            if (upgrade_btn_x <= x <= upgrade_btn_x + 120 and 
                upgrade_btn_y <= y <= upgrade_btn_y + 40):
                cost = 30 * self.selected_tower.level
                if self.money >= cost:
                    self.money -= cost
                    self.selected_tower.upgrade()
                    return True
        
        # Sell button
        if self.selected_tower:
            sell_btn_x = SCREEN_WIDTH - 140
            sell_btn_y = SCREEN_HEIGHT - 100
            if (sell_btn_x <= x <= sell_btn_x + 120 and 
                sell_btn_y <= y <= sell_btn_y + 40):
                refund = int(TOWER_COSTS[self.selected_tower.tower_type] * 0.7)
                self.money += refund
                self.towers.remove(self.selected_tower)
                self.selected_tower = None
                self.placing_tower = False
                return True
        
        return False
    
    def can_place_tower(self, x, y):
        # Check if on path
        for i in range(len(self.path) - 1):
            p1 = self.path[i]
            p2 = self.path[i + 1]
            
            # Simple check: distance from line segment
            dist = self.distance_to_line_segment(x, y, p1[0], p1[1], p2[0], p2[1])
            if dist < 30:
                return False
        
        # Check if too close to other towers
        for tower in self.towers:
            if math.hypot(tower.x - x, tower.y - y) < 40:
                return False
        
        # Check if within screen bounds
        if x < 30 or x > SCREEN_WIDTH - 30 or y < 30 or y > SCREEN_HEIGHT - 130:
            return False
        
        return True
    
    def distance_to_line_segment(self, px, py, x1, y1, x2, y2):
        """Calculate distance from point to line segment"""
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:  # Points are same
            return math.hypot(px - x1, py - y1)
        
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return math.hypot(px - closest_x, py - closest_y)
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Update wave manager
        self.wave_manager.update(self.enemies, self.path)
        
        # Update enemies
        for enemy in self.enemies[:]:
            result = enemy.update()
            if result == "reached_end":
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
        
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies, current_time, self.projectiles)
        
        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update(self.enemies)
            if not proj.active:
                self.projectiles.remove(proj)
        
        # Remove dead enemies and collect bounty
        for enemy in self.enemies[:]:
            if not enemy.alive:
                self.enemies.remove(enemy)
                if enemy.bounty:
                    self.money += enemy.bounty
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw path
        if len(self.path) > 1:
            for i in range(len(self.path) - 1):
                pygame.draw.line(self.screen, (50, 50, 50), 
                                self.path[i], self.path[i+1], 60)
        
        # Draw grid (optional)
        self.draw_grid()
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over or pause screen
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause_screen()
        
        pygame.display.flip()
    
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (SCREEN_WIDTH, y))
    
    def draw_ui(self):
        # Money and lives
        money_text = self.font.render(f"Money: ${self.money}", True, GREEN)
        lives_text = self.font.render(f"Lives: {self.lives}", True, RED)
        wave_text = self.font.render(f"Wave: {self.wave_manager.get_current_wave()}", True, YELLOW)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 35))
        self.screen.blit(wave_text, (10, 60))
        
        # Draw tower shop buttons
        tower_types = ['basic', 'sniper', 'splash', 'slow']
        button_width = 120
        button_height = 40
        start_y = SCREEN_HEIGHT - 100
        
        for i, t_type in enumerate(tower_types):
            btn_x = 20 + i * (button_width + 10)
            
            # Button background
            color = (60, 60, 60)
            if self.money >= TOWER_COSTS[t_type]:
                if self.placing_tower and self.tower_type == t_type:
                    color = (150, 150, 150)
                else:
                    color = (80, 80, 80)
            else:
                color = (40, 40, 40)
            
            pygame.draw.rect(self.screen, color, (btn_x, start_y, button_width, button_height))
            pygame.draw.rect(self.screen, (150, 150, 150), (btn_x, start_y, button_width, button_height), 2)
            
            # Tower type and cost
            cost_text = self.font.render(f"{t_type} (${TOWER_COSTS[t_type]})", True, WHITE)
            self.screen.blit(cost_text, (btn_x + 5, start_y + 10))
        
        # Start wave button
        start_btn_x = SCREEN_WIDTH - 140
        start_btn_y = SCREEN_HEIGHT - 100
        if not self.wave_manager.is_wave_active():
            start_color = (80, 80, 80)
            start_text = "Start Wave"
        else:
            start_color = (40, 40, 40)
            start_text = "Wave Active"
        
        pygame.draw.rect(self.screen, start_color, 
                        (start_btn_x, start_btn_y, 120, 40))
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (start_btn_x, start_btn_y, 120, 40), 2)
        text = self.font.render(start_text, True, WHITE)
        self.screen.blit(text, (start_btn_x + 5, start_btn_y + 10))
        
        # Tower actions (upgrade/sell) when selected
        if self.selected_tower:
            upgrade_cost = 30 * self.selected_tower.level
            upgrade_color = (80, 80, 80) if self.money >= upgrade_cost else (40, 40, 40)
            
            pygame.draw.rect(self.screen, upgrade_color, 
                            (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 60, 120, 40))
            pygame.draw.rect(self.screen, (150, 150, 150), 
                            (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 60, 120, 40), 2)
            
            upgrade_text = self.font.render(f"Upgrade (${upgrade_cost})", True, WHITE)
            self.screen.blit(upgrade_text, (SCREEN_WIDTH - 135, SCREEN_HEIGHT - 55))
            
            # Sell button
            refund = int(TOWER_COSTS[self.selected_tower.tower_type] * 0.7)
            pygame.draw.rect(self.screen, (80, 80, 80), 
                            (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 100, 120, 40))
            pygame.draw.rect(self.screen, (150, 150, 150), 
                            (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 100, 120, 40), 2)
            
            sell_text = self.font.render(f"Sell (${refund})", True, WHITE)
            self.screen.blit(sell_text, (SCREEN_WIDTH - 135, SCREEN_HEIGHT - 95))
        
        # Tower info when selected
        if self.selected_tower:
            stats = self.selected_tower.stats
            info_lines = [
                f"Type: {self.selected_tower.tower_type.title()}",
                f"Level: {self.selected_tower.level}",
                f"Damage: {stats['damage']}",
                f"Range: {stats['range']}",
                f"Cooldown: {stats['fire_rate']}"
            ]
            
            for i, line in enumerate(info_lines):
                text = self.font.render(line, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 200, 20 + i * 20))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, text_rect)
        
        score_text = self.font.render(f"Wave Reached: {self.wave_manager.get_current_wave()}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("Press SPACE to restart", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSED", True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
    
    def reset(self):
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.game_over = False
        self.paused = False
        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.selected_tower = None
        self.placing_tower = False
        self.tower_type = None
        self.wave_manager = WaveManager()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()