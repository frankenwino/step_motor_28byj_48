# Architecture

<!-- metadata:type=architecture, audience=ai-agents, scope=system-design -->

## Overview

The project follows a flat, procedural architecture with no class hierarchy. A single module handles all motor control logic through module-level state and standalone functions.

## Architectural Pattern

**Pattern:** Procedural scripting with module-level initialization

The module initializes GPIO hardware at import time (module-level side effects), then exposes functions for motor control. This is a common pattern for simple Raspberry Pi hardware drivers.

## System Architecture

```mermaid
graph TB
    subgraph "Python Application"
        A[User Script / __main__] --> B[left/right/test functions]
        B --> C[Step1-Step8 functions]
    end
    subgraph "Hardware Abstraction"
        C --> D[RPi.GPIO Library]
    end
    subgraph "Physical Hardware"
        D --> E[GPIO Pins 6, 13, 19, 26]
        E --> F[ULN2003 Driver Board]
        F --> G[28BYJ-48 Stepper Motor]
    end
```

## Execution Flow

```mermaid
sequenceDiagram
    participant User as User/Script
    participant Module as step_motor_28byj_48
    participant GPIO as RPi.GPIO
    participant Motor as 28BYJ-48

    Note over Module: Module import triggers GPIO init
    Module->>GPIO: setmode(BCM)
    Module->>GPIO: setup(IN1-IN4, OUT)
    Module->>GPIO: output(IN1-IN4, False)

    User->>Module: left(512) or right(512)
    loop 512 cycles
        loop 8 steps per cycle
            Module->>GPIO: output(pins, True/False)
            Module->>Module: sleep(0.001)
        end
    end
    GPIO->>Motor: Electrical signals
    Motor-->>User: Physical rotation
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Module-level GPIO init | Simple usage — import and call. No setup ceremony needed |
| Half-step sequence | Smoother rotation and higher resolution than full-step |
| Hardcoded pins | Single-purpose driver for a specific wiring configuration |
| No class abstraction | Minimal complexity for a single-motor use case |
| `time = 0.001` global | Simple speed control via module-level variable |

## Constraints

- **Single motor only:** Pin assignments are hardcoded; cannot drive multiple motors simultaneously
- **Import side effects:** Importing the module immediately configures GPIO, which fails on non-Pi hardware
- **No error handling:** No validation of step counts, no GPIO error recovery
- **Blocking execution:** `left()` and `right()` block until all steps complete
