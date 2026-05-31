"""Driver for 28BYJ-48 stepper motor via ULN2003 driver board."""

from __future__ import annotations

from time import sleep
from typing import ClassVar

import RPi.GPIO as GPIO  # type: ignore[import-untyped]


class StepMotor28BYJ48:
    """28BYJ-48 stepper motor controller.

    Args:
        pin1: GPIO BCM pin for ULN2003 IN1.
        pin2: GPIO BCM pin for ULN2003 IN2.
        pin3: GPIO BCM pin for ULN2003 IN3.
        pin4: GPIO BCM pin for ULN2003 IN4.
        delay: Seconds between steps (controls speed).

    Raises:
        ValueError: If delay is not positive.
    """

    _SEQUENCE: ClassVar[tuple[tuple[int, ...], ...]] = (
        (0, 0, 0, 1),
        (0, 0, 1, 1),
        (0, 0, 1, 0),
        (0, 1, 1, 0),
        (0, 1, 0, 0),
        (1, 1, 0, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 1),
    )

    STEPS_PER_REVOLUTION: ClassVar[int] = 512

    def __init__(
        self,
        pin1: int = 6,
        pin2: int = 13,
        pin3: int = 19,
        pin4: int = 26,
        delay: float = 0.001,
    ) -> None:
        if delay <= 0:
            raise ValueError("delay must be positive")
        self._pins = (pin1, pin2, pin3, pin4)
        self._delay = delay
        self._closed = False
        GPIO.setmode(GPIO.BCM)
        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def __enter__(self) -> StepMotor28BYJ48:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _run_steps(self, steps: int, *, forward: bool) -> None:
        """Execute step cycles in the given direction.

        Args:
            steps: Number of full step cycles.
            forward: True for counter-clockwise, False for clockwise.

        Raises:
            ValueError: If steps is not positive.
            RuntimeError: If motor is closed.
        """
        if self._closed:
            raise RuntimeError("Motor is closed")
        if steps <= 0:
            raise ValueError("steps must be positive")
        sequence = self._SEQUENCE if forward else self._SEQUENCE[::-1]
        for _ in range(steps):
            for state in sequence:
                for pin, value in zip(self._pins, state):
                    GPIO.output(pin, value)
                sleep(self._delay)

    def left(self, steps: int) -> None:
        """Rotate counter-clockwise by step cycles.

        Args:
            steps: Number of full step cycles (512 = 360°).
        """
        self._run_steps(steps, forward=True)

    def right(self, steps: int) -> None:
        """Rotate clockwise by step cycles.

        Args:
            steps: Number of full step cycles (512 = 360°).
        """
        self._run_steps(steps, forward=False)

    def rotate(self, degrees: float) -> None:
        """Rotate motor by degrees.

        Positive degrees = clockwise, negative = counter-clockwise.
        Zero degrees is a no-op.

        Args:
            degrees: Angle to rotate.

        Raises:
            RuntimeError: If motor is closed.
        """
        if self._closed:
            raise RuntimeError("Motor is closed")
        if degrees == 0:
            return
        steps = round(abs(degrees) / 360 * self.STEPS_PER_REVOLUTION)
        if steps == 0:
            return
        self._run_steps(steps, forward=degrees < 0)

    def close(self) -> None:
        """Release GPIO resources.

        Safe to call multiple times.
        """
        if not self._closed:
            self._closed = True
            GPIO.cleanup(list(self._pins))
