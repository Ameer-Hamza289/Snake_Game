# 🔧 Hardware Setup Guide - Enhanced Snake Game

## 📦 Component List

### Required Components
| Component | Quantity | Description |
|-----------|----------|-------------|
| Arduino Uno R3 | 1 | Main microcontroller |
| Analog Joystick Module | 1 | For snake movement control |
| Buzzer | 1 | Active or passive buzzer |
| LED | 1 | Status indicator (or use built-in) |
| Push Buttons | 2 | Start and Reset buttons |
| Breadboard | 1 | Half-size breadboard |
| Jumper Wires | 10-15 | Male-to-male wires |
| USB Cable | 1 | Type A to B for Arduino |

## 🔌 Pin Connections

### Analog Joystick Module
```
Joystick Pin → Arduino Pin
VCC  → 5V
GND  → GND
VRx  → A0 (X-axis)
VRy  → A1 (Y-axis)
SW   → Not used (optional for future)
```

### Push Buttons
```
Start Button:
Pin 1 → GND
Pin 2 → Digital Pin 7

Reset Button:
Pin 1 → GND
Pin 2 → Digital Pin 6
```

### Audio & Visual
```
Buzzer:
Positive → Digital Pin 8
Negative → GND

LED:
Anode (+) → Digital Pin 13
Cathode (-) → GND
(Or use built-in LED on pin 13)
```

## 🛠️ Assembly Steps

### Step 1: Power Distribution
1. Connect Arduino 5V to breadboard positive rail (red)
2. Connect Arduino GND to breadboard negative rail (blue)

### Step 2: Joystick Connection
1. Place joystick module on breadboard
2. Connect VCC to positive rail
3. Connect GND to negative rail
4. Use jumper wires:
   - VRx to Arduino A0
   - VRy to Arduino A1

### Step 3: Button Setup
1. Insert both push buttons on breadboard
2. Connect one pin of each button to negative rail
3. Connect other pins:
   - Start button → Arduino Pin 7
   - Reset button → Arduino Pin 6

### Step 4: Audio Setup
1. Connect buzzer positive to Arduino Pin 8
2. Connect buzzer negative to negative rail

### Step 5: LED Setup
1. Connect LED anode to Arduino Pin 13
2. Connect LED cathode to negative rail
3. Alternatively: Use built-in LED on Arduino

## 🔍 Circuit Diagram

```
        Arduino Uno
    ┌─────────────────┐
    │                 │
    │   Digital Pins  │
    │   ┌───────────┐ │
    │ 13│LED        │ │ ← Status LED
    │ 12│           │ │
    │ 11│           │ │
    │ 10│           │ │
    │  9│           │ │
    │  8│BUZZER     │ │ ← Sound output
    │  7│START BTN  │ │ ← Start/Pause
    │  6│RESET BTN  │ │ ← Reset game
    │   └───────────┘ │
    │                 │
    │   Analog Pins   │
    │   ┌───────────┐ │
    │ A5│           │ │
    │ A4│           │ │
    │ A3│           │ │
    │ A2│           │ │
    │ A1│JOY Y-AXIS │ │ ← Joystick Y
    │ A0│JOY X-AXIS │ │ ← Joystick X
    │   └───────────┘ │
    │                 │
    │   Power         │
    │   5V ─────────────── VCC Rail
    │   GND ──────────────── GND Rail
    └─────────────────┘
```

## ⚙️ Calibration

### Joystick Center Values
1. Upload the Arduino code
2. Open Serial Monitor (115200 baud)
3. Keep joystick at center position
4. Note the X and Y values being printed
5. If values are not around 512:
   - Update `JOY_CENTER_X` in code
   - Update `JOY_CENTER_Y` in code

### Sensitivity Adjustment
If joystick is too sensitive:
- Increase `JOY_DEADZONE` (default: 100)
- Increase `JOY_THRESHOLD` (default: 200)

## 🔧 Testing

### Component Testing
Run these tests before full assembly:

**Joystick Test:**
```cpp
void setup() {
  Serial.begin(9600);
}
void loop() {
  Serial.print("X: ");
  Serial.print(analogRead(A0));
  Serial.print(" Y: ");
  Serial.println(analogRead(A1));
  delay(200);
}
```

**Button Test:**
```cpp
void setup() {
  Serial.begin(9600);
  pinMode(7, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
}
void loop() {
  Serial.print("Start: ");
  Serial.print(digitalRead(7));
  Serial.print(" Reset: ");
  Serial.println(digitalRead(6));
  delay(200);
}
```

## ⚡ Power Requirements

- **Total Current**: ~50-100mA
- **Voltage**: 5V (USB powered)
- **Components Power Draw**:
  - Arduino Uno: ~20mA
  - Joystick: ~5mA
  - Buzzer: ~20mA (when active)
  - LED: ~20mA
  - Buttons: 0mA (when not pressed)

## 🚨 Troubleshooting

### Common Issues

**Joystick not responding:**
- Check VCC and GND connections
- Verify A0, A1 connections
- Test with multimeter for 0-5V range

**Buttons not working:**
- Ensure one pin connects to GND
- Check internal pull-up is enabled in code
- Test button continuity

**No sound from buzzer:**
- Check polarity (if passive buzzer)
- Verify pin 8 connection
- Test with simple tone() function

**LED not lighting:**
- Check polarity (anode to pin 13)
- Verify GND connection
- Test with digitalWrite(13, HIGH)

### Debugging Steps
1. Check all connections with multimeter
2. Verify Arduino power (LED should be on)
3. Test individual components separately
4. Use Serial Monitor to debug values
5. Check for loose connections

## 📐 Physical Layout Tips

### Breadboard Organization
- Keep power rails on edges
- Group related components
- Use color-coded wires:
  - Red: 5V/VCC
  - Black: GND
  - Other colors: Signal wires

### Wire Management
- Keep wires short and neat
- Avoid crossing wires when possible
- Label connections for easy debugging

## 🔄 Alternative Configurations

### Without Breadboard
- Use jumper wires directly to components
- Less organized but functional

### Using Different Pins
If pins are occupied, you can change:
- Joystick pins (update in code)
- Button pins (update pin definitions)
- Buzzer pin (update BUZZER_PIN)

### Component Substitutions
- **LED**: Can use built-in Arduino LED (pin 13)
- **Buzzer**: Active or passive buzzers work
- **Buttons**: Any momentary push buttons

## ✅ Final Checklist

Before testing:
- [ ] All connections secure
- [ ] No short circuits
- [ ] Correct pin assignments
- [ ] Arduino powered via USB
- [ ] Code uploaded successfully
- [ ] Serial Monitor working (115200 baud)
- [ ] Python client ready to run

**Ready to play! 🎮** 