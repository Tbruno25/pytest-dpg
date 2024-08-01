from abc import ABC, abstractmethod

import dearpygui.dearpygui as dpg
import pyautogui


class Command(ABC):
    """Abstract base class for automation commands."""

    @abstractmethod
    def command(self) -> None:
        """Execute the command's specific action."""
        ...

    def execute(self) -> None:
        self.command()
        dpg.render_dearpygui_frame()


class MouseMove(Command):
    """Command to move the mouse to a specific position."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        pyautogui.moveTo(self.x, self.y)


class MouseDown(Command):
    """Command to perform a mouse down action."""

    def command(self) -> None:
        pyautogui.mouseDown()


class MouseUp(Command):
    """Command to perform a mouse up action."""

    def command(self) -> None:
        pyautogui.mouseUp()


class MouseClick(Command):
    """Command to perform a mouse click action."""

    def command(self) -> None:
        MouseDown().execute()
        MouseUp().execute()


class MoveAndClick(Command):
    """Command to move the mouse to a position and click."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        MouseMove(self.x, self.y).execute()
        MouseClick().execute()


class ClickAndReturn(Command):
    """Command to click at a position and return to the starting position."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        starting_position = pyautogui.position()
        MoveAndClick(self.x, self.y).execute()
        MouseMove(*starting_position).execute()


class ClickAndDrag(Command):
    """Command to perform a click and drag action."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def command(self) -> None:
        MouseDown().execute()
        MouseMove(self.x, self.y).execute()
        MouseUp().execute()