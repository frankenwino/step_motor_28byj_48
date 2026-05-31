# Workflows

<!-- metadata:type=workflows, audience=ai-agents, scope=processes -->

## Motor Control Workflow

### Typical Usage Flow

```mermaid
flowchart TD
    A[Create StepMotor28BYJ48] --> B[GPIO initialized]
    B --> C{Use motor}
    C --> D["rotate(degrees)"]
    C --> E["left(steps) / right(steps)"]
    D --> F[_run_steps converts and executes]
    E --> F
    F --> G{More operations?}
    G -->|Yes| C
    G -->|No| H["close()"]
    H --> I[GPIO cleaned up]
```

### Rotation Execution

```mermaid
flowchart TD
    A["_run_steps(steps, forward)"] --> B{_closed?}
    B -->|Yes| C[raise RuntimeError]
    B -->|No| D{steps > 0?}
    D -->|No| E[raise ValueError]
    D -->|Yes| F[Select sequence direction]
    F --> G{forward?}
    G -->|Yes| H[Use _SEQUENCE as-is]
    G -->|No| I[Use _SEQUENCE reversed]
    H --> J[Loop: steps x 8 states]
    I --> J
    J --> K[GPIO.output for each pin]
    K --> L["sleep(delay)"]
    L --> M{More states?}
    M -->|Yes| K
    M -->|No| N{More cycles?}
    N -->|Yes| J
    N -->|No| O[Return]
```

### Degree-to-Steps Conversion

```mermaid
flowchart LR
    A[degrees] --> B["steps = round(abs(degrees) / 360 x 512)"]
    B --> C{degrees > 0?}
    C -->|Yes| D["_run_steps(steps, forward=False) Clockwise"]
    C -->|No| E["_run_steps(steps, forward=True) Counter-clockwise"]
```

## Context Manager Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Motor as StepMotor28BYJ48
    participant GPIO as RPi.GPIO

    User->>Motor: with StepMotor28BYJ48() as motor
    Motor->>GPIO: setmode, setup, output
    Motor-->>User: motor instance

    User->>Motor: motor.rotate(360)
    Motor->>GPIO: output calls x 512 x 8

    Note over User,Motor: Block exits (normal or exception)
    Motor->>Motor: __exit__ calls close()
    Motor->>GPIO: cleanup([6, 13, 19, 26])
```

## Development Workflows

### Testing

```mermaid
flowchart LR
    A[pytest] --> B[conftest.py patches RPi.GPIO]
    B --> C[test_motor.py runs 23 tests]
    C --> D[Coverage report at 98 percent]
```

### Quality Checks

```mermaid
flowchart LR
    A[make lint] --> B[ruff check]
    C[make typecheck] --> D[mypy --strict]
    E[make test] --> F[pytest]
    G[make coverage] --> H[pytest --cov --cov-fail-under=90]
```

### Build and Install

```mermaid
flowchart LR
    A["pip install -e .[dev]"] --> B[hatchling builds]
    B --> C[Package + dev tools installed]
```
