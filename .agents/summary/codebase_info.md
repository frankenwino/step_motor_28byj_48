# Codebase Information

<!-- metadata:type=overview, audience=ai-agents, scope=project-wide -->

## Project Identity

| Field | Value |
|-------|-------|
| Name | step-motor-28byj-48 |
| Author | Andrew Browne |
| Version | 1.0.0 |
| License | GPL-3.0-or-later |
| Status | Beta (Development Status :: 4) |
| Repository | https://github.com/frankenwino/step_motor_28byj_48 |
| Python | ≥ 3.9 |

## Purpose

Python driver for the 28BYJ-48 stepper motor connected to a Raspberry Pi via the ULN2003 driver board. Provides a class-based interface to rotate the motor by degrees or step cycles, with configurable pins and speed.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9+ |
| Hardware Interface | RPi.GPIO (BCM mode) |
| Build System | hatchling |
| Test Framework | pytest + pytest-cov |
| Type Checking | mypy (strict mode) |
| Linting | ruff |
| Documentation | Sphinx (alabaster theme) |
| Task Runner | GNU Make |

## Directory Structure

```
step_motor_28byj_48/
├── step_motor_28byj_48/          # Main package
│   ├── __init__.py               # Exports StepMotor28BYJ48, __version__
│   ├── motor.py                  # Motor controller class
│   └── py.typed                  # PEP 561 type marker
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # GPIO mock fixture
│   └── test_motor.py             # 23 tests (98% coverage)
├── docs/                         # Sphinx documentation source
│   └── conf.py
├── pyproject.toml                # Build config, deps, tool settings
├── Makefile                      # Development task automation
├── README.md                     # Project documentation
├── AGENTS.md                     # AI agent context file
├── CONTRIBUTING.rst              # Contribution guidelines
├── HISTORY.rst                   # Changelog
├── AUTHORS.rst                   # Contributors
└── LICENSE                       # GPLv3
```

## Hardware Requirements

- Raspberry Pi (any model with GPIO header)
- 28BYJ-48 stepper motor
- ULN2003 driver board
- 5V power supply for motor

## GPIO Pin Mapping (defaults)

| ULN2003 Pin | GPIO (BCM) |
|-------------|-----------|
| IN1 | 6 |
| IN2 | 13 |
| IN3 | 19 |
| IN4 | 26 |
| - | GND |
| + | 5V |
