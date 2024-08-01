import queue
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import dearpygui.dearpygui as dpg
import multiprocess as mp
import pyautogui

import pytest_dpg
from pytest_dpg.commands import ClickAndDrag, ClickAndReturn, MouseMove
from pytest_dpg.dpg_helpers import (
    DPGItem,
    get_item_center_position,
    get_item_value,
    get_item_with_or_near_text,
    get_slider_position,
)


class TestReceiver:
    """Class for receiving and executing GUI test commands."""

    def __init__(
        self, func: Callable, command_queue: mp.Queue, result_queue: mp.Queue,
    ) -> None:
        """
        Initialize the TestReceiver.

        Args:
            func: The function that initializes the GUI to be tested.
            command_queue: A multiprocessing Queue for receiving commands.
            result_queue: A multiprocessing Queue for sending results.
        """
        self._func = func
        self.command_queue = command_queue
        self.result_queue = result_queue

    def _process_command(self) -> None:
        """Process a command from the command queue if available."""
        try:
            command = self.command_queue.get_nowait()
            result = self._execute_command(command)
            self.result_queue.put(result)
        except queue.Empty:
            pass

    def _execute_command(self, command: str | tuple) -> Any:
        """
        Execute a command.

        Args:
            command: A string or tuple representing the command to execute.

        Returns:
            The result of the command execution.
        """
        if isinstance(command, tuple):
            method, *args = command
            return getattr(self, method)(*args)

        return getattr(self, command)()

    def _patched_loop(self) -> None:
        """Run the patched DPG main loop, processing commands between frames."""
        dpg.set_viewport_always_top(True)
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            self._process_command()

    def set_target(self, func: Callable) -> None:
        """
        Set the target function for the GUI test.

        Args:
            func: The function that initializes the GUI to be tested.
        """
        self._func = func

    def start_gui(self) -> None:
        """Start the GUI with patched DPG loop and configured PyAutoGUI settings."""
        pyautogui.PAUSE = pytest_dpg.PAUSE
        pyautogui.MINIMUM_DURATION = pyautogui.MINIMUM_DURATION
        with patch.object(dpg, "start_dearpygui", new=self._patched_loop):
            self._func()

    def click(self, item: int) -> None:
        """
        Click on a DPG item.

        Args:
            item: The ID of the DPG item to click.
        """
        x, y = get_item_center_position(item)
        return ClickAndReturn(x, y).execute()

    def click_button(self, label: str) -> None:
        """
        Click a button with the given label.

        Args:
            label: The label of the button to click.
        """
        button = get_item_with_or_near_text(DPGItem.BUTTON, label)
        return self.click(button)

    def click_tab(self, label: str) -> None:
        """
        Click a tab with the given label.

        Args:
            label: The label of the tab to click.
        """
        tab = get_item_with_or_near_text(DPGItem.TAB, label)
        return self.click(tab)

    def drag_slider(self, label: str, value: int) -> None:
        """
        Drag a slider to the specified value.

        Args:
            label: The label of the slider to drag.
            value: The value to drag the slider to.
        """
        slider = get_item_with_or_near_text(DPGItem.SLIDER, label)
        curr_x, curr_y = get_slider_position(slider, get_item_value(slider))
        target_x, target_y = get_slider_position(slider, value)
        MouseMove(curr_x, curr_y).execute()
        return ClickAndDrag(target_x, target_y).execute()