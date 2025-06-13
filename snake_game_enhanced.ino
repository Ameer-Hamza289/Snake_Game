/*
 * ENHANCED SNAKE GAME - Arduino Uno
 * Course: Programming Fundamentals
 * Features: Joystick Control, Sound Effects, High Scores, Multiple Levels
 * Display: Serial Monitor / Python GUI
 * Author: Jawad's Project
 */

#include <EEPROM.h>

// Game Configuration
#define GRID_WIDTH 40
#define GRID_HEIGHT 20
#define MAX_SNAKE_LENGTH 100
#define EEPROM_HIGH_SCORE_ADDR 0

// Hardware Pins
#define JOY_X_PIN A0
#define JOY_Y_PIN A1
#define BUZZER_PIN 8
#define LED_PIN 13
#define BUTTON_START 7
#define BUTTON_RESET 6

// Joystick Configuration
const int JOY_CENTER_X = 512;
const int JOY_CENTER_Y = 512;
const int JOY_DEADZONE = 100;
const int JOY_THRESHOLD = 200;

// Game States
enum GameState {
  MENU,
  PLAYING,
  PAUSED,
  GAME_OVER,
  HIGH_SCORE_SCREEN
};

// Directions
enum Direction {
  RIGHT = 0,
  UP = 1,
  LEFT = 2,
  DOWN = 3
};

// Game Variables
struct Point {
  int x, y;
};

struct Snake {
  Point body[MAX_SNAKE_LENGTH];
  int length;
  Direction direction;
  Direction nextDirection;
};

struct GameData {
  Snake snake;
  Point food;
  int score;
  int highScore;
  int level;
  int speed;
  GameState state;
  unsigned long lastMoveTime;
  unsigned long lastInputTime;
  bool soundEnabled;
  int lives;
};

GameData game;

// Sound Frequencies
const int FREQ_EAT = 1000;
const int FREQ_GAME_OVER = 200;
const int FREQ_LEVEL_UP = 1500;
const int FREQ_MOVE = 100;

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_START, INPUT_PULLUP);
  pinMode(BUTTON_RESET, INPUT_PULLUP);
  
  // Initialize random seed
  randomSeed(analogRead(A2));
  
  // Initialize game
  initializeGame();
  
  // Welcome message
  Serial.println("=== ENHANCED SNAKE GAME ===");
  Serial.println("Controls: Joystick for movement");
  Serial.println("Start Button: Begin/Pause");
  Serial.println("Reset Button: Restart");
  Serial.println("s: Toggle Sound");
  Serial.println("=============================");
  
  playStartupSound();
}

void loop() {
  handleInput();
  updateGame();
  sendGameData();
  delay(10); // Small delay for stability
}

void initializeGame() {
  // Load high score from EEPROM
  game.highScore = EEPROM.read(EEPROM_HIGH_SCORE_ADDR) | 
                   (EEPROM.read(EEPROM_HIGH_SCORE_ADDR + 1) << 8);
  
  // Initialize snake
  game.snake.length = 3;
  game.snake.direction = RIGHT;
  game.snake.nextDirection = RIGHT;
  
  // Starting position (center-left)
  game.snake.body[0] = {GRID_WIDTH/4, GRID_HEIGHT/2};
  game.snake.body[1] = {GRID_WIDTH/4-1, GRID_HEIGHT/2};
  game.snake.body[2] = {GRID_WIDTH/4-2, GRID_HEIGHT/2};
  
  // Initialize game state
  game.score = 0;
  game.level = 1;
  game.speed = 200; // milliseconds
  game.state = MENU;
  game.lastMoveTime = 0;
  game.lastInputTime = 0;
  game.soundEnabled = true;
  game.lives = 3;
  
  spawnFood();
}

void handleInput() {
  // Handle joystick input
  if (millis() - game.lastInputTime > 50) { // Debounce
    handleJoystickInput();
    game.lastInputTime = millis();
  }
  
  // Handle button input
  handleButtonInput();
  
  // Handle serial commands
  if (Serial.available()) {
    char cmd = Serial.read();
    handleSerialCommand(cmd);
  }
}

void handleJoystickInput() {
  int xVal = analogRead(JOY_X_PIN);
  int yVal = analogRead(JOY_Y_PIN);
  
  int xDiff = xVal - JOY_CENTER_X;
  int yDiff = yVal - JOY_CENTER_Y;
  
  // Apply deadzone
  if (abs(xDiff) < JOY_DEADZONE && abs(yDiff) < JOY_DEADZONE) {
    return;
  }
  
  if (game.state != PLAYING) return;
  
  Direction newDirection = game.snake.direction;
  
  // Determine primary direction
  if (abs(xDiff) > abs(yDiff)) {
    // Horizontal movement
    if (xDiff > JOY_THRESHOLD && game.snake.direction != LEFT) {
      newDirection = RIGHT;
    } else if (xDiff < -JOY_THRESHOLD && game.snake.direction != RIGHT) {
      newDirection = LEFT;
    }
  } else {
    // Vertical movement
    if (yDiff > JOY_THRESHOLD && game.snake.direction != UP) {
      newDirection = DOWN;
    } else if (yDiff < -JOY_THRESHOLD && game.snake.direction != DOWN) {
      newDirection = UP;
    }
  }
  
  game.snake.nextDirection = newDirection;
}

void handleButtonInput() {
  static bool startPressed = false;
  static bool resetPressed = false;
  
  // Start/Pause button
  if (digitalRead(BUTTON_START) == LOW && !startPressed) {
    startPressed = true;
    
    switch (game.state) {
      case MENU:
        game.state = PLAYING;
        playSound(FREQ_LEVEL_UP, 100);
        break;
      case PLAYING:
        game.state = PAUSED;
        break;
      case PAUSED:
        game.state = PLAYING;
        break;
      case GAME_OVER:
        resetGame();
        break;
    }
  } else if (digitalRead(BUTTON_START) == HIGH) {
    startPressed = false;
  }
  
  // Reset button
  if (digitalRead(BUTTON_RESET) == LOW && !resetPressed) {
    resetPressed = true;
    resetGame();
  } else if (digitalRead(BUTTON_RESET) == HIGH) {
    resetPressed = false;
  }
}

void handleSerialCommand(char cmd) {
  switch (cmd) {
    case 's':
    case 'S':
      game.soundEnabled = !game.soundEnabled;
      Serial.print("Sound: ");
      Serial.println(game.soundEnabled ? "ON" : "OFF");
      break;
    case 'r':
    case 'R':
      resetGame();
      break;
    case 'p':
    case 'P':
      if (game.state == PLAYING) game.state = PAUSED;
      else if (game.state == PAUSED) game.state = PLAYING;
      break;
  }
}

void updateGame() {
  if (game.state != PLAYING) return;
  
  // Check if it's time to move
  if (millis() - game.lastMoveTime >= game.speed) {
    moveSnake();
    game.lastMoveTime = millis();
  }
}

void moveSnake() {
  // Update direction
  game.snake.direction = game.snake.nextDirection;
  
  // Calculate new head position
  Point newHead = game.snake.body[0];
  
  switch (game.snake.direction) {
    case RIGHT: newHead.x++; break;
    case LEFT:  newHead.x--; break;
    case DOWN:  newHead.y++; break;
    case UP:    newHead.y--; break;
  }
  
  // Check wall collision
  if (newHead.x < 0 || newHead.x >= GRID_WIDTH || 
      newHead.y < 0 || newHead.y >= GRID_HEIGHT) {
    handleCollision();
    return;
  }
  
  // Check self collision
  for (int i = 0; i < game.snake.length; i++) {
    if (newHead.x == game.snake.body[i].x && 
        newHead.y == game.snake.body[i].y) {
      handleCollision();
      return;
    }
  }
  
  // Move snake body
  for (int i = game.snake.length - 1; i > 0; i--) {
    game.snake.body[i] = game.snake.body[i-1];
  }
  
  game.snake.body[0] = newHead;
  
  // Check food collision
  if (newHead.x == game.food.x && newHead.y == game.food.y) {
    eatFood();
  }
}

void eatFood() {
  // Grow snake
  if (game.snake.length < MAX_SNAKE_LENGTH) {
    game.snake.length++;
  }
  
  // Increase score
  game.score += game.level * 10;
  
  // Play sound
  playSound(FREQ_EAT, 100);
  
  // Flash LED
  digitalWrite(LED_PIN, HIGH);
  delay(50);
  digitalWrite(LED_PIN, LOW);
  
  // Check level up
  if (game.score % 100 == 0) {
    levelUp();
  }
  
  // Spawn new food
  spawnFood();
}

void levelUp() {
  game.level++;
  game.speed = max(50, game.speed - 20); // Increase speed, minimum 50ms
  
  playSound(FREQ_LEVEL_UP, 200);
  
  Serial.print("LEVEL UP! Level: ");
  Serial.println(game.level);
}

void handleCollision() {
  game.lives--;
  
  if (game.lives <= 0) {
    gameOver();
  } else {
    // Reset snake position but keep score
    game.snake.length = 3;
    game.snake.direction = RIGHT;
    game.snake.nextDirection = RIGHT;
    
    game.snake.body[0] = {GRID_WIDTH/4, GRID_HEIGHT/2};
    game.snake.body[1] = {GRID_WIDTH/4-1, GRID_HEIGHT/2};
    game.snake.body[2] = {GRID_WIDTH/4-2, GRID_HEIGHT/2};
    
    playSound(300, 500); // Warning sound
    delay(1000); // Brief pause
  }
}

void gameOver() {
  game.state = GAME_OVER;
  
  // Check and save high score
  if (game.score > game.highScore) {
    game.highScore = game.score;
    saveHighScore();
    Serial.println("NEW HIGH SCORE!");
  }
  
  playGameOverSound();
  
  Serial.println("GAME OVER!");
  Serial.print("Final Score: ");
  Serial.println(game.score);
  Serial.print("High Score: ");
  Serial.println(game.highScore);
}

void spawnFood() {
  bool validPosition = false;
  
  while (!validPosition) {
    game.food.x = random(0, GRID_WIDTH);
    game.food.y = random(0, GRID_HEIGHT);
    
    validPosition = true;
    
    // Make sure food doesn't spawn on snake
    for (int i = 0; i < game.snake.length; i++) {
      if (game.food.x == game.snake.body[i].x && 
          game.food.y == game.snake.body[i].y) {
        validPosition = false;
        break;
      }
    }
  }
}

void resetGame() {
  initializeGame();
  Serial.println("Game Reset!");
}

void saveHighScore() {
  EEPROM.write(EEPROM_HIGH_SCORE_ADDR, game.highScore & 0xFF);
  EEPROM.write(EEPROM_HIGH_SCORE_ADDR + 1, (game.highScore >> 8) & 0xFF);
}

void sendGameData() {
  // Send game state as JSON for easy parsing
  Serial.print("{");
  Serial.print("\"state\":");
  Serial.print(game.state);
  Serial.print(",\"score\":");
  Serial.print(game.score);
  Serial.print(",\"highScore\":");
  Serial.print(game.highScore);
  Serial.print(",\"level\":");
  Serial.print(game.level);
  Serial.print(",\"lives\":");
  Serial.print(game.lives);
  Serial.print(",\"snake\":[");
  
  for (int i = 0; i < game.snake.length; i++) {
    if (i > 0) Serial.print(",");
    Serial.print("{\"x\":");
    Serial.print(game.snake.body[i].x);
    Serial.print(",\"y\":");
    Serial.print(game.snake.body[i].y);
    Serial.print("}");
  }
  
  Serial.print("],\"food\":{\"x\":");
  Serial.print(game.food.x);
  Serial.print(",\"y\":");
  Serial.print(game.food.y);
  Serial.print("},\"direction\":");
  Serial.print(game.snake.direction);
  Serial.println("}");
}

// Sound Functions
void playSound(int frequency, int duration) {
  if (!game.soundEnabled) return;
  
  tone(BUZZER_PIN, frequency, duration);
}

void playStartupSound() {
  if (!game.soundEnabled) return;
  
  int melody[] = {262, 294, 330, 349, 392, 440, 494, 523};
  for (int i = 0; i < 8; i++) {
    tone(BUZZER_PIN, melody[i], 100);
    delay(120);
  }
}

void playGameOverSound() {
  if (!game.soundEnabled) return;
  
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, FREQ_GAME_OVER, 300);
    delay(300);
    noTone(BUZZER_PIN);
    delay(100);
  }
} 