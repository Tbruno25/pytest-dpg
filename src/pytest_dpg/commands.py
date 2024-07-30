from abc import ABC, abstractmethod

import dearpygui.dearpygui as dpg
import pyautogui

class Command(ABC):
    @abstractmethod
    def command(self) -> None:
        ...

    def execute(self) -> None:
        self.command()
        dpg.render_dearpygui_frame()


class MouseMove(Command):
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        pyautogui.moveTo(self.x, self.y)


class MouseDown(Command):
    def command(self) -> None:
        pyautogui.mouseDown()


class MouseUp(Command):
    def command(self) -> None:
        pyautogui.mouseUp()


class MouseClick(Command):
    def command(self):
        MouseDown().execute()
        MouseUp().execute()


class MoveAndClick(Command):
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self):
        MouseMove(self.x, self.y).execute()
        MouseClick().execute()


class ClickAndReturn(Command):
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        starting_position = pyautogui.position()
        MoveAndClick(self.x, self.y).execute()
        MouseMove(*starting_position).execute()


class ClickAndDrag(Command):
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        MouseDown().execute()
        MouseMove(self.x, self.y).execute()
        MouseUp().execute()
