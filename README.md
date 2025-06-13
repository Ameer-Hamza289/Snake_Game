# 🐍 Enhanced Snake Game - Arduino Uno

## 🎮 Project Overview
A fully enhanced Snake Game using Arduino Uno with joystick control and laptop display. Features include sound effects, high scores, multiple lives, and progressive difficulty.

## ✨ Features

### Core Game Features
- **🕹️ Joystick Control**: Analog joystick with configurable deadzone
- **🏆 High Score System**: Persistent storage using EEPROM
- **❤️ Multiple Lives**: 3 lives per game
- **📈 Progressive Difficulty**: Speed increases with level
- **🔊 Sound Effects**: Buzzer for game events
- **💡 Visual Feedback**: LED indicators

### Enhanced Features
- **📏 40×20 Game Grid**: Large playing field
- **🖥️ Real-time Display**: Python GUI for smooth graphics
- **🎯 Game States**: Menu, Playing, Paused, Game Over
- **📡 JSON Communication**: Structured data transfer
- **⌨️ Keyboard Commands**: Additional controls via laptop

## 🔧 Hardware Requirements

### Components
- Arduino Uno R3
- Analog Joystick Module
- Buzzer (Active or Passive)
- LED
- 2× Push Buttons
- Breadboard
- Jumper Wires
- USB Cable

### Pin Configuration
```
Joystick X-axis: A0
Joystick Y-axis: A1
Buzzer: Pin 8
Status LED: Pin 13
Start Button: Pin 7
Reset Button: Pin 6
```

## 🔌 Circuit Diagram

```
Arduino Uno Connections:
┌─────────────────┐
│     ARDUINO     │
│                 │
│ A0 ──── JOY_X   │
│ A1 ──── JOY_Y   │
│ D7 ──── START   │
│ D6 ──── RESET   │
│ D8 ──── BUZZER  │
│ D13 ─── LED     │
│                 │
│ 5V ──── VCC     │
│ GND ─── GND     │
└─────────────────┘
```

## 💻 Software Setup

### Arduino IDE
1. Install Arduino IDE
2. Upload `snake_game_enhanced.ino` to Arduino

### Python Display Client
1. Install Python 3.7+
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the display client:
```bash
python snake_display.py COM3
```

## 🎯 Controls

### Hardware Controls
- **Joystick**: Move snake (Up/Down/Left/Right)
- **Start Button**: Begin game / Pause / Resume
- **Reset Button**: Restart game

### Keyboard Commands
- **S**: Toggle sound on/off
- **P**: Pause/Resume game
- **R**: Reset game

## 📊 Game Mechanics

### Scoring System
- **Food**: 10 × Current Level points
- **Level Up**: Every 100 points
- **Speed**: Increases with each level

### Lives System
- Start with 3 lives
- Lose life on collision
- Game over when all lives lost

## 🚀 Quick Start

1. **Hardware Setup**: Connect components per circuit diagram
2. **Upload Code**: Load Arduino sketch
3. **Install Python**: `pip install pygame pyserial`
4. **Run Game**: `python snake_display.py COM3`
5. **Play**: Use joystick to control snake!

## 🔊 Audio Features

- **Startup**: Musical scale
- **Food**: High pitch beep  
- **Level Up**: Rising tone
- **Game Over**: Descending tones

## 🛠️ Troubleshooting

### Common Issues
- **Arduino not detected**: Check USB cable and port
- **Joystick too sensitive**: Increase deadzone value
- **No display**: Verify COM port in Python command
- **No sound**: Check buzzer connections

## 📁 Project Files

```
Snake_Game_Arduino/
├── snake_game_enhanced.ino    # Arduino code
├── snake_display.py           # Python display
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 👨‍💻 Author
**Course**: Programming Fundamentals  
**Project**: Jawad's Enhanced Snake Game  

## 🎯 Learning Outcomes
- Embedded C/C++ programming
- Real-time input processing
- Serial communication
- Game state management
- Hardware interfacing

**Happy Gaming! 🐍🎮** 