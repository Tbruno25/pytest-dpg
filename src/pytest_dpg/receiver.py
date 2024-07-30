import queue
from typing import Any, Callable
from unittest.mock import patch

import dearpygui.dearpygui as dpg
import multiprocess as mp

from pytest_dpg.commands import (ClickAndDrag, ClickAndReturn, MouseMove,
                                 MoveAndClick)
from pytest_dpg.dpg_helpers import (DPGItem, get_item_center_position,
                                    get_item_value, get_item_with_or_near_text,
                                    get_slider_position)
import pytest_dpg
import pyautogui

class TestReceiver:
    def __init__(
        self, func: Callable, command_queue: mp.Queue, result_queue: mp.Queue
    ) -> None:
        self._func = func
        self.command_queue = command_queue
        self.result_queue = result_queue

    def _process_command(self) -> None:
        try:
            command = self.command_queue.get_nowait()
            result = self._execute_command(command)
            self.result_queue.put(result)
        except queue.Empty:
            pass

    def _execute_command(self, command) -> Any:
        if isinstance(command, tuple):
            method, *args = command
            return getattr(self, method)(*args)
        else:
            return getattr(self, command)()

    def _patched_loop(self):
        dpg.set_viewport_always_top(True)
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            self._process_command()
        
    def set_target(self, func: Callable) -> None:
        self._func = func

    def start_gui(self):
        pyautogui.PAUSE = pytest_dpg.PAUSE
        pyautogui.MINIMUM_DURATION = pyautogui.MINIMUM_DURATION
        with patch.object(dpg, "start_dearpygui", new=self._patched_loop):
            self._func()

    def click(self, item: int) -> None:
        x, y = get_item_center_position(item)
        return ClickAndReturn(x, y).execute()

    def click_button(self, label: str) -> None:
        button = get_item_with_or_near_text(DPGItem.BUTTON, label)
        return self.click(button)

    def click_tab(self, label: str) -> None:
        tab = get_item_with_or_near_text(DPGItem.TAB, label)
        return self.click(tab)

    def drag_slider(self, label: str, value: int) -> None:        
        slider = get_item_with_or_near_text(DPGItem.SLIDER, label)
        curr_x, curr_y = get_slider_position(slider, get_item_value(slider))
        target_x, target_y = get_slider_position(slider, value)
        MouseMove(curr_x, curr_y).execute()
        return ClickAndDrag(target_x, target_y).execute()
