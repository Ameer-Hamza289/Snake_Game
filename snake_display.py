"""
Enhanced Snake Game Display Client
Receives game data from Arduino via Serial and displays it
"""

import pygame
import serial
import json
import sys
import time
from threading import Thread
import queue

# Initialize Pygame
pygame.init()

# Display Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_WIDTH = 40
GRID_HEIGHT = 20
CELL_SIZE = min(WINDOW_WIDTH // GRID_WIDTH, WINDOW_HEIGHT // GRID_HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Game States
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
HIGH_SCORE_SCREEN = 4

class SnakeDisplay:
    def __init__(self, serial_port='COM3', baud_rate=115200):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Snake Game")
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Serial communication
        self.data_queue = queue.Queue()
        self.game_data = None
        
        try:
            self.serial_conn = serial.Serial(serial_port, baud_rate, timeout=0.1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"Connected to {serial_port}")
            
            # Start serial thread
            self.serial_thread = Thread(target=self.read_serial_data, daemon=True)
            self.serial_thread.start()
            
        except serial.SerialException as e:
            print(f"Failed to connect to {serial_port}: {e}")
            print("Running in demo mode...")
            print("Available ports:")
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for port in ports:
                print(f"  {port.device}")
            self.serial_conn = None
    
    def read_serial_data(self):
        buffer = ""
        while self.running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting:
                    data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8')
                    buffer += data
                    
                    # Process complete JSON objects
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip().startswith('{'):
                            try:
                                game_data = json.loads(line.strip())
                                self.data_queue.put(game_data)
                            except json.JSONDecodeError:
                                pass  # Skip invalid JSON
                        else:
                            print(line.strip())  # Print non-JSON messages
                            
            except Exception as e:
                print(f"Serial read error: {e}")
                time.sleep(0.1)
    
    def update_game_data(self):
        while not self.data_queue.empty():
            try:
                self.game_data = self.data_queue.get_nowait()
            except queue.Empty:
                break
    
    def draw_grid(self):
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (0, y), (GRID_WIDTH * CELL_SIZE, y))
    
    def draw_snake(self, snake_data):
        for i, segment in enumerate(snake_data):
            x = segment['x'] * CELL_SIZE
            y = segment['y'] * CELL_SIZE
            
            # Different colors for head and body
            if i == 0:  # Head
                color = GREEN
                pygame.draw.rect(self.screen, color, 
                               (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                # Draw eyes
                pygame.draw.circle(self.screen, WHITE, 
                                 (x + CELL_SIZE//3, y + CELL_SIZE//3), 2)
                pygame.draw.circle(self.screen, WHITE, 
                                 (x + 2*CELL_SIZE//3, y + CELL_SIZE//3), 2)
            else:  # Body
                brightness = max(100, 255 - i * 5)
                color = (0, brightness, 0)
                pygame.draw.rect(self.screen, color, 
                               (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
    
    def draw_food(self, food_data):
        x = food_data['x'] * CELL_SIZE
        y = food_data['y'] * CELL_SIZE
        
        # Animated food
        time_factor = pygame.time.get_ticks() / 200
        size_offset = int(2 * abs(pygame.math.cos(time_factor)))
        
        pygame.draw.circle(self.screen, RED, 
                         (x + CELL_SIZE//2, y + CELL_SIZE//2), 
                         CELL_SIZE//2 - 2 + size_offset)
        pygame.draw.circle(self.screen, YELLOW, 
                         (x + CELL_SIZE//2, y + CELL_SIZE//2), 
                         CELL_SIZE//4)
    
    def draw_hud(self, game_data):
        hud_y = GRID_HEIGHT * CELL_SIZE + 10
        
        # Score
        score_text = self.font_medium.render(f"Score: {game_data['score']}", 
                                           True, WHITE)
        self.screen.blit(score_text, (10, hud_y))
        
        # High Score
        high_score_text = self.font_medium.render(f"High: {game_data['highScore']}", 
                                                True, YELLOW)
        self.screen.blit(high_score_text, (200, hud_y))
        
        # Level
        level_text = self.font_medium.render(f"Level: {game_data['level']}", 
                                           True, BLUE)
        self.screen.blit(level_text, (350, hud_y))
        
        # Lives
        lives_text = self.font_medium.render(f"Lives: {game_data['lives']}", 
                                           True, RED)
        self.screen.blit(lives_text, (500, hud_y))
        
        # Direction indicator
        directions = ["→", "↑", "←", "↓"]
        dir_text = self.font_large.render(directions[game_data['direction']], 
                                        True, GREEN)
        self.screen.blit(dir_text, (650, hud_y - 10))
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.font_large.render("ENHANCED SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "Joystick: Move Snake",
            "Start Button: Begin Game",
            "Reset Button: Restart",
            "S: Toggle Sound",
            "P: Pause/Resume",
            "",
            "Press START to begin!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = WHITE if instruction else BLACK
            text = self.font_small.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 200 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_game_over(self, game_data):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {game_data['score']}", 
                                           True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 280))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if game_data['score'] == game_data['highScore']:
            hs_text = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
        else:
            hs_text = self.font_medium.render(f"High Score: {game_data['highScore']}", 
                                            True, YELLOW)
        hs_rect = hs_text.get_rect(center=(WINDOW_WIDTH//2, 320))
        self.screen.blit(hs_text, hs_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press START or R to restart", 
                                            True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, 400))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_paused(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        paused_text = self.font_large.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(paused_text, paused_rect)
        
        # Resume instruction
        resume_text = self.font_small.render("Press START or P to resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.serial_conn:
                    if event.key == pygame.K_s:
                        self.serial_conn.write(b's')
                    elif event.key == pygame.K_r:
                        self.serial_conn.write(b'r')
                    elif event.key == pygame.K_p:
                        self.serial_conn.write(b'p')
    
    def run(self):
        while self.running:
            self.handle_input()
            self.update_game_data()
            
            self.screen.fill(BLACK)
            
            if self.game_data:
                state = self.game_data['state']
                
                if state == MENU:
                    self.draw_menu()
                elif state == PLAYING:
                    self.draw_grid()
                    self.draw_snake(self.game_data['snake'])
                    self.draw_food(self.game_data['food'])
                    self.draw_hud(self.game_data)
                elif state == PAUSED:
                    self.draw_grid()
                    self.draw_snake(self.game_data['snake'])
                    self.draw_food(self.game_data['food'])
                    self.draw_hud(self.game_data)
                    self.draw_paused()
                elif state == GAME_OVER:
                    self.draw_grid()
                    self.draw_snake(self.game_data['snake'])
                    self.draw_food(self.game_data['food'])
                    self.draw_hud(self.game_data)
                    self.draw_game_over(self.game_data)
            else:
                # No data received yet
                waiting_text = self.font_medium.render("Waiting for Arduino...", True, WHITE)
                waiting_rect = waiting_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                self.screen.blit(waiting_text, waiting_rect)
                
                # Show connection info
                if self.serial_conn:
                    port_text = self.font_small.render(f"Connected to: {self.serial_conn.port}", True, GREEN)
                else:
                    port_text = self.font_small.render("No serial connection", True, RED)
                port_rect = port_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
                self.screen.blit(port_text, port_rect)
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        if self.serial_conn:
            self.serial_conn.close()
        pygame.quit()

if __name__ == "__main__":
    # You may need to change COM3 to your Arduino's port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 'COM3'  # Default port, change as needed
    
    print("Starting Enhanced Snake Game Display...")
    print(f"Attempting to connect to port: {port}")
    print("If connection fails, try different port (e.g., COM4, COM5)")
    
    game = SnakeDisplay(port)
    game.run() 