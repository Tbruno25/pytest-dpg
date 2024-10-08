import time
from collections.abc import Callable
from typing import Any

import multiprocess as mp

from pytest_dpg.receiver import ReceiverError, TestReceiver


class TestInvoker:
    """Class for invoking GUI tests and managing the test process."""

    def __init__(self) -> None:
        self._command_queue: mp.Queue = mp.Queue()
        self._result_queue: mp.Queue = mp.Queue()
        self._process: mp.Process | None = None
        self._receiver: TestReceiver | None = None

    def _send_command(self, command: tuple) -> Any:
        """
        Send a command to the TestReceiver and get the result.

        Args:
            command: A tuple representing the command to send.

        Returns:
            The result of the command execution.

        Raises:
            RuntimeError: If set_target() hasn't been called.
        """
        if self._receiver is None:
            msg = "Must run set_target() method before starting"
            raise RuntimeError(msg)
        self._receiver.command_queue.put(command)
        result = self._receiver.result_queue.get()

        if isinstance(result, ReceiverError):
            print(f"Exception occurred in GUI process:\n{result}")
            raise result

        return result

    def set_target(self, func: Callable) -> None:
        """
        Set the target function for the GUI test.

        Args:
            func: The function that initializes the GUI to be tested.
        """
        self._receiver = TestReceiver(func, self._command_queue, self._result_queue)

    def start_gui(self) -> None:
        """
        Start the GUI in a separate process.

        Raises:
            RuntimeError: If set_target() hasn't been called.
        """
        if self._receiver is None:
            msg = "Must run set_target() method before starting"
            raise RuntimeError(msg)
        self._process = mp.Process(target=self._receiver.start_gui)
        self._process.start()
        time.sleep(1)

    def stop_gui(self) -> None:
        """Stop the GUI process if it's running."""
        if self._process:
            self._process.kill()

    def click_button(self, label: str) -> None:
        """
        Click a button with the given label.

        Args:
            label: The label of the button to click.
        """
        return self._send_command(("click_button", label))

    def click_combo(self, label: str) -> None:
        """
        Click a combo box with the given label.

        Args:
            label: The label of the combo box to click.
        """
        return self._send_command(("click_combo", label))

    def click_header(self, label: str) -> None:
        """
        Click a collapsing header with the given label.

        Args:
            label: The label of the collapsing header to click.
        """
        return self._send_command(("click_header", label))

    def click_input_text(self, label: str) -> None:
        """
        Click an input text box with the given label.

        Args:
            label: The label of the input text box to click.
        """
        return self._send_command(("click_input_text", label))

    def click_tab(self, label: str) -> None:
        """
        Click a tab with the given label.

        Args:
            label: The label of the tab to click.
        """
        return self._send_command(("click_tab", label))

    def drag_slider(self, label: str, value: int) -> None:
        """
        Drag a slider to the specified value.

        Args:
            label: The label of the slider to drag.
            value: The value to drag the slider to.
        """
        return self._send_command(("drag_slider", label, value))

    def set_combo(self, label: str, value: str) -> None:
        """
        Set the value of a combo box with the given label.

        Args:
            label: The label of the combo box to set.
            value: The value to set in the combo box.
        """
        return self._send_command(("set_combo", label, value))

    def set_input_text(self, label: str, text: str) -> None:
        """
        Set the text of an input text box with the given label.

        Args:
            label: The label of the input text box to set.
            text: The text to set in the input text box.
        """
        return self._send_command(("set_input_text", label, text))
