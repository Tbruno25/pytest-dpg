import multiprocess as mp
import pytest

from pytest_dpg.invoker import TestInvoker

# Use the external multiprocess library for better
# serialization compatibility across different platforms
mp.set_start_method("spawn")


@pytest.fixture()
def dpgtester():
    """
    Pytest fixture that provides a TestInvoker instance for DPG testing.

    This fixture creates a TestInvoker, yields it for use in tests,
    and ensures proper cleanup after the test is complete.

    Yields:
        TestInvoker: An instance of TestInvoker for interacting with the DPG application.

    Example:
        def test_my_gui(dpgtester):
            dpgtester.set_target(my_gui_function)
            dpgtester.start_gui()
            dpgtester.click_button("OK")
            # Add assertions here
    """
    tester = TestInvoker()
    yield tester
    tester.stop_gui()