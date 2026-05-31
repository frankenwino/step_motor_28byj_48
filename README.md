# step_motor_28byj_48

Raspberry Pi driver for the 28BYJ-48 stepper motor with ULN2003 driver board.

## Installation

```bash
pip install step-motor-28byj-48
```

Or for development:

```bash
git clone https://github.com/frankenwino/step_motor_28byj_48.git
cd step_motor_28byj_48
pip install -e ".[dev]"
```

## Hardware Setup

Connect the ULN2003 driver board to the Raspberry Pi:

| ULN2003 | GPIO (BCM) |
|---------|-----------|
| IN1 | 6 |
| IN2 | 13 |
| IN3 | 19 |
| IN4 | 26 |
| - | GND |
| + | 5V |

> **Tip:** Run `pinout` at the terminal for a GPIO pin layout diagram.

## Usage

```python
from step_motor_28byj_48 import StepMotor28BYJ48

# Context manager ensures GPIO cleanup
with StepMotor28BYJ48() as motor:
    motor.rotate(360)     # Full rotation clockwise
    motor.rotate(-180)    # Half rotation counter-clockwise
    motor.left(128)       # 90° counter-clockwise by step cycles
    motor.right(256)      # 180° clockwise by step cycles

# Custom pins and speed
motor = StepMotor28BYJ48(pin1=17, pin2=27, pin3=22, pin4=23, delay=0.002)
motor.rotate(90)
motor.close()
```

### Rotation Reference

| Degrees | Step cycles |
|---------|-------------|
| 360° | 512 |
| 180° | 256 |
| 90° | 128 |

## API

### `StepMotor28BYJ48(pin1=6, pin2=13, pin3=19, pin4=26, delay=0.001)`

Create a motor controller. Raises `ValueError` if delay ≤ 0.

### `motor.rotate(degrees)`

Rotate by angle. Positive = clockwise, negative = counter-clockwise.

### `motor.left(steps)` / `motor.right(steps)`

Rotate by step cycles. 512 steps = 360°.

### `motor.close()`

Release GPIO resources. Also called automatically by the context manager.

## Development

```bash
make test        # Run tests
make lint        # Check with ruff
make typecheck   # Run mypy
make coverage    # Tests with coverage report
make format      # Auto-format code
```

## License

GNU General Public License v3 — see [LICENSE](LICENSE).

## Credits

- [scraptopower.co.uk](http://www.scraptopower.co.uk/Raspberry-Pi/how-to-connect-stepper-motors-a-raspberry-pi)
- [custom-build-robots](https://github.com/custom-build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi)
