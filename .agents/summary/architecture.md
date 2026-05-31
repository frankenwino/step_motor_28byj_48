# Architecture

<!-- metadata:type=architecture, audience=ai-agents, scope=system-design -->

## Overview

Single-class architecture encapsulating all motor state and control logic. No module-level side effects — GPIO is initialized only when a `StepMotor28BYJ48` instance is created.

## Architectural Pattern

**Pattern:** Object-oriented hardware driver with context manager protocol

The class encapsulates GPIO state, provides a clean lifecycle (init → use → close), and supports Python's `with` statement for automatic resource cleanup.

## System Architecture

```mermaid
graph TB
    subgraph "Python Application"
        A[User Code] --> B[StepMotor28BYJ48]
        B --> C[_run_steps internal method]
        C --> D[_SEQUENCE class variable]
    end
    subgraph "Hardware Abstraction"
        C --> E[RPi.GPIO Library]
    end
    subgraph "Physical Hardware"
        E --> F[GPIO Pins 6, 13, 19, 26]
        F --> G[ULN2003 Driver Board]
        G --> H[28BYJ-48 Stepper Motor]
    end
```

## Class Design

```mermaid
classDiagram
    class StepMotor28BYJ48 {
        +STEPS_PER_REVOLUTION: int = 512
        -_SEQUENCE: tuple
        -_pins: tuple
        -_delay: float
        -_closed: bool
        +__init__(pin1, pin2, pin3, pin4, delay)
        +__enter__() StepMotor28BYJ48
        +__exit__(*args)
        +rotate(degrees: float)
        +left(steps: int)
        +right(steps: int)
        +close()
        -_run_steps(steps, forward)
    }
```

## Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Motor as StepMotor28BYJ48
    participant GPIO as RPi.GPIO

    User->>Motor: __init__(pins, delay)
    Motor->>GPIO: setmode(BCM)
    Motor->>GPIO: setup(pins, OUT)
    Motor->>GPIO: output(pins, LOW)

    User->>Motor: rotate(90)
    Motor->>Motor: Convert 90 degrees to 128 steps
    loop 128 cycles
        loop 8 sequence entries
            Motor->>GPIO: output(pins, state)
            Motor->>Motor: sleep(delay)
        end
    end

    User->>Motor: close()
    Motor->>GPIO: cleanup([pins])
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Class-based (not procedural) | Encapsulates state, supports multiple motors, enables context manager |
| Data-driven step sequence | Single tuple table + loop replaces 8 separate functions |
| Per-pin GPIO cleanup | `GPIO.cleanup([pins])` avoids interfering with other GPIO users |
| `_closed` flag | Prevents use-after-close bugs with clear `RuntimeError` |
| No print statements | Clean library behavior; users add their own logging |
| Configurable pins | Supports non-default wiring and multiple motors |

## Constraints

- **RPi.GPIO import at module level:** Importing `motor.py` requires RPi.GPIO to be available (or mocked)
- **Blocking execution:** `left()`, `right()`, and `rotate()` block until all steps complete
- **Single-threaded:** No thread safety; concurrent calls from multiple threads are unsafe
- **No async support:** Blocking `sleep()` calls; not compatible with asyncio event loops
