# Documentation Index

<!-- metadata:type=index, audience=ai-agents, scope=navigation -->

## How to Use This Documentation

This index is the **primary entry point** for AI assistants working with the `step_motor_28byj_48` codebase. Use this file to:

1. Understand the project at a glance (see Quick Summary below)
2. Determine which documentation file contains the information you need
3. Navigate to detailed documentation for specific topics

**Recommendation:** Load this file first. For most questions, the summaries below will be sufficient. Only load individual files when you need deeper detail on a specific topic.

## Quick Summary

This is a Python driver for the **28BYJ-48 stepper motor** connected to a **Raspberry Pi** via a **ULN2003 driver board**. It provides a single class `StepMotor28BYJ48` with methods to rotate by degrees or step cycles. The motor is controlled via GPIO pins (default: 6, 13, 19, 26) using a half-step sequence. 512 step cycles = 360 degree rotation. Built with modern Python tooling (pyproject.toml, mypy strict, ruff, pytest).

## Documentation Files

| File | Purpose | Consult When... |
|------|---------|-----------------|
| [codebase_info.md](codebase_info.md) | Project identity, tech stack, directory layout, hardware requirements | You need project metadata, version info, directory structure, or pin mappings |
| [architecture.md](architecture.md) | System design, class diagram, execution flow, design decisions | You need to understand how the system is structured or why decisions were made |
| [components.md](components.md) | Class details, method table, half-step sequence, rotation math | You need specifics about what each method does or the step sequence |
| [interfaces.md](interfaces.md) | Public API, constructor params, usage examples, error handling | You need to know how to use the library or what parameters methods accept |
| [data_models.md](data_models.md) | Instance state, class variables, state transitions | You need to understand the data/state managed by the class |
| [workflows.md](workflows.md) | Motor control flows, development workflows, context manager lifecycle | You need to understand execution order, build/test processes |
| [dependencies.md](dependencies.md) | Runtime/dev dependencies, platform requirements, testing without hardware | You need to know what the project depends on or how to test off-Pi |

## Key Facts for Quick Reference

- **Entry point:** `step_motor_28byj_48/motor.py` (class `StepMotor28BYJ48`)
- **Public methods:** `rotate(degrees)`, `left(steps)`, `right(steps)`, `close()`
- **Context manager:** `with StepMotor28BYJ48() as motor:`
- **GPIO pins (BCM defaults):** IN1=6, IN2=13, IN3=19, IN4=26
- **Rotation:** 512 cycles = 360 degrees, 256 = 180, 128 = 90
- **Speed:** Controlled by `delay` parameter (default 0.001 seconds)
- **Import note:** `motor.py` imports RPi.GPIO at top level; mock before importing for off-Pi testing
- **Build system:** hatchling (pyproject.toml)
- **Type safety:** mypy strict, PEP 561 compliant (py.typed marker)

## Cross-References

- For **wiring instructions** see [codebase_info.md](codebase_info.md) (GPIO Pin Mapping)
- For **how left/right differ** see [components.md](components.md) (Direction Logic)
- For **the step sequence pattern** see [components.md](components.md) (Half-Step Sequence Table)
- For **how to test without a Pi** see [dependencies.md](dependencies.md) (Testing Without Hardware)
- For **error types and conditions** see [interfaces.md](interfaces.md) (Error Handling)
- For **development commands** see [workflows.md](workflows.md) (Development Workflows)
