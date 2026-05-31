# AGENTS.md

> Raspberry Pi Python driver for the 28BYJ-48 stepper motor via ULN2003 driver board.

## Directory Map

```
step_motor_28byj_48/
├── step_motor_28byj_48/
│   ├── __init__.py       # Exports StepMotor28BYJ48, __version__
│   ├── motor.py          # ← ALL motor control logic (StepMotor28BYJ48 class)
│   └── py.typed          # PEP 561 type marker
├── tests/
│   ├── conftest.py       # mock_gpio fixture (patches RPi.GPIO)
│   └── test_motor.py     # 23 tests, 98% coverage
├── docs/conf.py          # Sphinx config
├── pyproject.toml        # Build config, deps, tool settings
├── Makefile              # Dev task runner
└── HISTORY.rst           # Changelog
```

## Key Entry Point

**`step_motor_28byj_48/motor.py`** — Single class `StepMotor28BYJ48`:
- Data-driven half-step sequence (tuple table, not 8 separate functions)
- `__init__(pin1, pin2, pin3, pin4, delay)` — configurable pins and speed
- `rotate(degrees)` — positive=CW, negative=CCW
- `left(steps)` / `right(steps)` — by step cycles (512 = 360°)
- `close()` — releases GPIO; also via context manager
- Input validation: `ValueError` for bad params, `RuntimeError` after close

## Critical Gotchas

- **RPi.GPIO import at module level:** `motor.py` imports `RPi.GPIO` at the top. On non-Pi hardware, you must mock it before importing (see `tests/conftest.py` for the pattern).
- **Blocking calls:** `rotate()` and `left()`/`right()` block for the duration of rotation.
- **GPIO cleanup is per-pin:** Uses `GPIO.cleanup([pins])` not `GPIO.cleanup()` — won't interfere with other GPIO users.

## Hardware Wiring (BCM pin numbers)

| GPIO | ULN2003 |
|------|---------|
| 6 | IN1 |
| 13 | IN2 |
| 19 | IN3 |
| 26 | IN4 |

## Tooling (configured in pyproject.toml)

- **Lint:** `ruff check` (rules: E, F, I, UP, B; target py39)
- **Type check:** `mypy --strict`
- **Test:** `pytest` (with pytest-cov)
- **Build:** hatchling

## Detailed Documentation

See `.agents/summary/index.md` for architecture, component, and workflow docs.

## Custom Instructions
<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->
