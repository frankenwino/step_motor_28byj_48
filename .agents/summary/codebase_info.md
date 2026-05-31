# Codebase Information

<!-- metadata:type=overview, audience=ai-agents, scope=project-wide -->

## Project Identity

| Field | Value |
|-------|-------|
| Name | step_motor_28byj_48 |
| Author | Andrew Browne |
| Version | 0.1.0 |
| License | GNU General Public License v3 |
| Status | Pre-Alpha (Development Status :: 2) |
| Repository | https://github.com/frankenwino/step_motor_28byj_48 |

## Purpose

Python driver for the 28BYJ-48 stepper motor connected to a Raspberry Pi via the ULN2003 driver board. Provides functions to rotate the motor left or right by a specified number of step cycles.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python (2.7, 3.5–3.8) |
| Hardware Interface | RPi.GPIO (BCM mode) |
| Build System | setuptools |
| Test Framework | unittest |
| Linting | flake8 |
| Multi-env Testing | tox |
| Documentation | Sphinx (alabaster theme) |
| Versioning | bump2version |
| CI | Travis CI |
| Task Runner | GNU Make |

## Directory Structure

```
step_motor_28byj_48/
├── step_motor_28byj_48/          # Main package
│   ├── __init__.py               # Package metadata (author, version)
│   └── step_motor_28byj_48.py   # Motor control implementation
├── tests/                        # Unit tests (placeholder)
│   ├── __init__.py
│   └── test_step_motor_28byj_48.py
├── docs/                         # Sphinx documentation source
│   └── conf.py
├── setup.py                      # Package configuration
├── setup.cfg                     # bumpversion, flake8, wheel config
├── tox.ini                       # Multi-environment test config
├── Makefile                      # Development task automation
├── requirements.txt              # Runtime dependency (RPi.GPIO==0.7.0)
├── README.rst                    # PyPI/Sphinx readme
├── README.md                     # GitHub readme
├── CONTRIBUTING.rst              # Contribution guidelines
├── HISTORY.rst                   # Changelog
├── AUTHORS.rst                   # Contributors
├── LICENSE                       # GPLv3
└── MANIFEST.in                   # Source distribution manifest
```

## Hardware Requirements

- Raspberry Pi (any model with GPIO header)
- 28BYJ-48 stepper motor
- ULN2003 driver board
- 5V power supply for motor

## GPIO Pin Mapping

| ULN2003 Pin | GPIO (BCM) | Physical Function |
|-------------|-----------|-------------------|
| IN1 | 6 | Coil A |
| IN2 | 13 | Coil B |
| IN3 | 19 | Coil C |
| IN4 | 26 | Coil D |
| - | GND | Ground |
| + | 5V | Motor power |
