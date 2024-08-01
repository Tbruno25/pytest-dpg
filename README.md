<h1 align="center">
    <!-- Please provide path to your logo here -->
    <!-- <img src="" alt="Logo" width="200" height="200"> -->
  </a>
</h1>

<div align="center">
  pytest-dpg
  <br />
  <a href="https://github.com/tbruno25/pytest-dpg/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/tbruno25/pytest-dpg/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feature%3A+">Request a Feature</a>
  ·
  <a href="https://github.com/tbruno25/pytest-dpg/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br/>


[![PyPI version](https://img.shields.io/pypi/v/pytest-dpg?color=mediumseagreen)](https://pypi.org/project/pytest-dpg/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytest-dpg?color=mediumseagreen)](https://pypi.org/project/pytest-dpg/)
[![Stars](https://img.shields.io/github/stars/tbruno25/pytest-dpg?color=mediumseagreen)](https://github.com/Tbruno25/pytest-dpg/stargazers)
</div>

---


# About

`pytest-dpg` is a pytest plugin for testing DearPyGui (DPG) applications. 

## Features

- Automates user interactions like clicking buttons, switching tabs, and dragging sliders
- Runs GUI tests in a separate process for concurrency, stability, and isolation
- Easy to use API for interacting with DPG elements
- Requires no application code modifications

## Installation


[pipx](https://pypa.github.io/pipx/) is recommended although any package manager that supports `pyproject.toml` files can be used.

```bash
pipx install pytest-dpg
``` 

## How it works

pytest-dpg creates a controlled environment for testing before performing introspection on the application:

- **DPG Loop Patching**: `dpgtester` patches DearPyGui's main loop (`dpg.start_dearpygui()`) with a custom loop that allows for command insertion between frames.
- **Item Identification**: utilizes DPG's internal APIs to locate items based on their labels, values, or adjacent items. This allows it to (hopefully) find the correct screen coordinates for interactions.

## Usage
pytest-dpg automatically makes the pytest fixture `dpgtester` available for use

```python
def test_my_gui(dpgtester):
    # This function should setup and start your application when run
    func = your_gui_function

    # Start your GUI application
    dpgtester.set_target(func)
    dpgtester.start_gui()

    # Interact with GUI elements
    dpgtester.click_button("Submit")
    dpgtester.click_tab("Settings")
    dpgtester.drag_slider("Volume", 75)

```

## Limitations
While pytest-dpg aims to provide a robust testing solution for DearPyGui applications, there are some current limitations to be aware of:

- **Limited Application Support:**
only applications that utilize `dpg.start_dearpygui()` are curently supported
- **Limited Widget Support:** ***only*** the following widgets are currently supported
    - regular buttons
    - horizontal sliders
    - tabs

- **Complex Layouts:** Very complex or dynamically changing layouts might pose challenges for element identification and interaction.

We are continuously working on improving pytest-dpg and addressing these limitations. Contributions and feedback are always welcome!

## API Reference

### dpgtester

- `set_target(func: Callable)` Set the target function for the GUI test
- `start_gui()` Start the GUI in a separate process
- `python stop_gui()` Stop the GUI process if it's running
- `click_button(label: str)` Click a button with the given label
- `click_tab(label: str)` Click a tab with the given label
- `drag_slider(label: str, value: int)` Drag a slider to the specified value

### pytest_dpg
By default, dpgtester will execute actions as quickly as possible.
To slow down interactions, the following attributes can be increased
```python
import pytest_dpg

pytest_dpg.PAUSE = 0.25
pytest_dpg.MINIMUM_DURATION = 0.5
```

## Support

Reach out to the maintainer at one of the following places:
- [GitHub issues](https://github.com/tbruno25/pytest-dpg/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/tbruno25)

If you want to say **thank you** or/and support active development of pytest-dpg consider adding a [GitHub Star](https://github.com/tbruno25/pytest-dpg) to the project.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

- Fork the repository
- Create your feature branch (git checkout -b feature/AmazingFeature)
- Commit your changes (git commit -m 'Add some AmazingFeature')
- Push to the branch (git push origin feature/AmazingFeature)
- Open a Pull Request

For a full list of all authors and contributors, see [the contributors page](https://github.com/tbruno25/pytest-dpg/contributors).

## License

This project is licensed under the **GNU General Public License v3**.

See [LICENSE](LICENSE) for more information.