import time
from typing import Any, Callable

import multiprocess as mp

from pytest_dpg.receiver import TestReceiver


class TestInvoker:
    def __init__(self):
        self._command_queue: mp.Queue = mp.Queue()
        self._result_queue: mp.Queue = mp.Queue()
        self._process: mp.Process | None = None
        self._receiver: TestReceiver | None = None

    def _send_command(self, command: tuple) -> Any:
        if self._receiver is None:
            raise RuntimeError("Must run set_target() method before starting")
        self._receiver.command_queue.put(command)
        return self._receiver.result_queue.get()

    def set_target(self, func: Callable) -> None:
        self._receiver = TestReceiver(func, self._command_queue, self._result_queue)

    def start_gui(self):
        if self._receiver is None:
            raise RuntimeError("Must run set_target() method before starting")
        self._process = mp.Process(target=self._receiver.start_gui)
        self._process.start()
        time.sleep(1)

    def stop_gui(self):
        if self._process:
            self._process.kill()

    def click_button(self, label: str) -> None:
        return self._send_command(("click_button", label))

    def click_tab(self, label: str) -> None:
        return self._send_command(("click_tab", label))

    def drag_slider(self, label: str, value: int) -> None:
        return self._send_command(("drag_slider", label, value))
