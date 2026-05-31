"""Tests for StepMotor28BYJ48."""

from __future__ import annotations

from unittest.mock import MagicMock, call

import pytest


def _make_motor(mock_gpio: MagicMock, **kwargs: object) -> object:
    """Import and instantiate motor with mocked GPIO."""
    # Re-import to pick up the mocked RPi.GPIO
    import importlib

    import step_motor_28byj_48.motor as motor_module

    importlib.reload(motor_module)
    return motor_module.StepMotor28BYJ48(**kwargs)  # type: ignore[arg-type]


class TestInit:
    """Initialization tests."""

    def test_default_pins(self, mock_gpio: MagicMock) -> None:
        _make_motor(mock_gpio)
        setup_calls = [c for c in mock_gpio.setup.call_args_list]
        pins_setup = [c[0][0] for c in setup_calls]
        assert pins_setup == [6, 13, 19, 26]

    def test_custom_pins(self, mock_gpio: MagicMock) -> None:
        _make_motor(mock_gpio, pin1=17, pin2=27, pin3=22, pin4=23)
        pins_setup = [c[0][0] for c in mock_gpio.setup.call_args_list]
        assert pins_setup == [17, 27, 22, 23]

    def test_sets_bcm_mode(self, mock_gpio: MagicMock) -> None:
        _make_motor(mock_gpio)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)

    def test_pins_set_low(self, mock_gpio: MagicMock) -> None:
        _make_motor(mock_gpio)
        output_calls = mock_gpio.output.call_args_list
        expected = [call(pin, False) for pin in [6, 13, 19, 26]]
        assert output_calls == expected

    def test_invalid_delay_raises(self, mock_gpio: MagicMock) -> None:
        with pytest.raises(ValueError, match="delay must be positive"):
            _make_motor(mock_gpio, delay=0)

    def test_negative_delay_raises(self, mock_gpio: MagicMock) -> None:
        with pytest.raises(ValueError, match="delay must be positive"):
            _make_motor(mock_gpio, delay=-0.5)


class TestRotation:
    """Rotation tests."""

    def test_left_calls_gpio_output(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.left(1)  # type: ignore[union-attr]
        # 1 step cycle = 8 sequence entries × 4 pins = 32 output calls
        assert mock_gpio.output.call_count == 32

    def test_right_calls_gpio_output(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.right(1)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 32

    def test_left_sequence_forward(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.left(1)  # type: ignore[union-attr]
        # First step should set pins to sequence[0] = (0, 0, 0, 1)
        first_four = [c[0] for c in mock_gpio.output.call_args_list[:4]]
        assert first_four == [(6, 0), (13, 0), (19, 0), (26, 1)]

    def test_right_sequence_reversed(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.right(1)  # type: ignore[union-attr]
        # Reversed sequence: first entry is (1, 0, 0, 1)
        first_four = [c[0] for c in mock_gpio.output.call_args_list[:4]]
        assert first_four == [(6, 1), (13, 0), (19, 0), (26, 1)]

    def test_step_count_multiple_cycles(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.left(3)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 3 * 8 * 4

    def test_invalid_steps_raises(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        with pytest.raises(ValueError, match="steps must be positive"):
            motor.left(0)  # type: ignore[union-attr]

    def test_negative_steps_raises(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        with pytest.raises(ValueError, match="steps must be positive"):
            motor.right(-1)  # type: ignore[union-attr]


class TestRotateDegrees:
    """Tests for rotate() method."""

    def test_positive_degrees_clockwise(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.rotate(360)  # type: ignore[union-attr]
        # 512 cycles × 8 steps × 4 pins
        assert mock_gpio.output.call_count == 512 * 8 * 4
        # First entry should be reversed sequence (clockwise): (1, 0, 0, 1)
        first_four = [c[0] for c in mock_gpio.output.call_args_list[:4]]
        assert first_four == [(6, 1), (13, 0), (19, 0), (26, 1)]

    def test_negative_degrees_counterclockwise(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.rotate(-360)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 512 * 8 * 4
        # First entry should be forward sequence (CCW): (0, 0, 0, 1)
        first_four = [c[0] for c in mock_gpio.output.call_args_list[:4]]
        assert first_four == [(6, 0), (13, 0), (19, 0), (26, 1)]

    def test_90_degrees_is_128_cycles(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.rotate(90)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 128 * 8 * 4

    def test_180_degrees_is_256_cycles(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.rotate(180)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 256 * 8 * 4

    def test_zero_degrees_no_op(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        mock_gpio.output.reset_mock()
        motor.rotate(0)  # type: ignore[union-attr]
        assert mock_gpio.output.call_count == 0


class TestCleanup:
    """Cleanup and context manager tests."""

    def test_close_calls_gpio_cleanup(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        motor.close()  # type: ignore[union-attr]
        mock_gpio.cleanup.assert_called_once_with([6, 13, 19, 26])

    def test_close_idempotent(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        motor.close()  # type: ignore[union-attr]
        motor.close()  # type: ignore[union-attr]
        mock_gpio.cleanup.assert_called_once()

    def test_context_manager_calls_close(self, mock_gpio: MagicMock) -> None:
        import importlib

        import step_motor_28byj_48.motor as motor_module

        importlib.reload(motor_module)
        with motor_module.StepMotor28BYJ48():
            pass
        mock_gpio.cleanup.assert_called_once_with([6, 13, 19, 26])

    def test_use_after_close_raises(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        motor.close()  # type: ignore[union-attr]
        with pytest.raises(RuntimeError, match="Motor is closed"):
            motor.left(1)  # type: ignore[union-attr]

    def test_rotate_after_close_raises(self, mock_gpio: MagicMock) -> None:
        motor = _make_motor(mock_gpio)
        motor.close()  # type: ignore[union-attr]
        with pytest.raises(RuntimeError, match="Motor is closed"):
            motor.rotate(90)  # type: ignore[union-attr]
