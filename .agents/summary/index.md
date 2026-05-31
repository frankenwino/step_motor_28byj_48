# Documentation Index

<!-- metadata:type=index, audience=ai-agents, scope=navigation -->

## How to Use This Documentation

This index is the **primary entry point** for AI assistants working with the `step_motor_28byj_48` codebase. Use this file to:

1. Understand the project at a glance (see Quick Summary below)
2. Determine which documentation file contains the information you need
3. Navigate to detailed documentation for specific topics

**Recommendation:** Load this file first. For most questions, the summaries below will be sufficient. Only load individual files when you need deeper detail on a specific topic.

## Quick Summary

This is a Python driver for the **28BYJ-48 stepper motor** connected to a **Raspberry Pi** via a **ULN2003 driver board**. It's a single-module, procedural library with 11 functions (8 step functions + left/right/test). The motor is controlled via GPIO pins 6, 13, 19, 26 using a half-step sequence. 512 step cycles = 360° rotation.

## Documentation Files

| File | Purpose | Consult When... |
|------|---------|-----------------|
| [codebase_info.md](codebase_info.md) | Project identity, tech stack, directory layout, hardware requirements | You need project metadata, version info, directory structure, or pin mappings |
| [architecture.md](architecture.md) | System design, execution flow, design decisions, constraints | You need to understand how the system is structured or why decisions were made |
| [components.md](components.md) | Detailed function documentation, half-step sequence table, rotation math | You need specifics about what each function does or the step sequence |
| [interfaces.md](interfaces.md) | Public API, function signatures, usage examples, integration points | You need to know how to use the library or what parameters functions accept |
| [data_models.md](data_models.md) | Module state, implicit data structures, GPIO state transitions | You need to understand the data/state managed by the module |
| [workflows.md](workflows.md) | Motor control flows, development workflows, import side effects | You need to understand execution order, build/test/release processes |
| [dependencies.md](dependencies.md) | Runtime/dev dependencies, platform requirements, known issues | You need to know what the project depends on or what's needed to run it |

## Key Facts for Quick Reference

- **Entry point:** `step_motor_28byj_48/step_motor_28byj_48.py`
- **Public functions:** `left(step)`, `right(step)`, `test(move_right=512, move_left=512)`
- **GPIO pins (BCM):** IN1=6, IN2=13, IN3=19, IN4=26
- **Rotation:** 512 cycles = 360°, 256 = 180°, 128 = 90°
- **Speed:** Controlled by `time = 0.001` (seconds between steps)
- **Import warning:** Importing the module initializes GPIO — fails on non-Pi hardware
- **Dependency gap:** RPi.GPIO is in requirements.txt but not in setup.py's install_requires

## Cross-References

- For **wiring instructions** → [codebase_info.md](codebase_info.md) (GPIO Pin Mapping)
- For **how left/right differ** → [components.md](components.md) (Control Functions) or [workflows.md](workflows.md) (rotation flowcharts)
- For **the step sequence pattern** → [components.md](components.md) (Half-Step Sequence Table) or [data_models.md](data_models.md) (Implicit Data)
- For **why tests can't run locally** → [dependencies.md](dependencies.md) (Platform Requirements) + [architecture.md](architecture.md) (Constraints)
- For **release process** → [workflows.md](workflows.md) (Release workflow)
