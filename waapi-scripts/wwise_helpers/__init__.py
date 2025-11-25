"""Helper utilities for interacting with the Wwise Authoring API (WAAPI).

The functions in this module wrap a couple of common workflows that are used
throughout the repository:

* Establishing a :class:`~waapi.WaapiClient` using the connection information
  stored in the local Wwise configuration file.
* Showing Tkinter based dialogs that report the progress of the scripts or ask
  the user for additional information.
* Retrieving the current clipboard content and the objects selected in the
  Wwise UI.

Historically these helpers were implemented without type hints or detailed
documentation which made them harder to reuse.  The annotations and docstrings
added here make the intent of each helper explicit and allow type checkers to
spot incorrect usages in client code.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from typing import Any, Callable, Dict, List, Optional

import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog
from waapi import WaapiClient

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


def set_client(ip: str = "127.0.0.1") -> WaapiClient:
    """Return a :class:`~waapi.WaapiClient` connected to the local Wwise host.

    The WAAPI port can be customised inside Wwise.  This helper inspects the
    Wwise settings file and uses the configured port if one is present.  When no
    custom port is found we fall back to the default ``8080``.

    Parameters
    ----------
    ip:
        The IPv4 address of the Wwise machine.  The default of
        ``"127.0.0.1"`` connects to the local host.

    Returns
    -------
    WaapiClient
        A client instance that can be used to make WAAPI calls.
    """

    port = "8080"
    wwise_settings = os.getenv("APPDATA", "") + r"\Audiokinetic\Wwise\Wwise.wsettings"
    tree = ET.ElementTree(file=wwise_settings)
    root = tree.getroot()
    for child in root[0][0][0]:
        if "Waapi\\WampPort" in child.attrib["Name"]:
            port = child.attrib["Value"]
    waapi_port = f"ws://{ip}:{port}/waapi"
    print(f"Client set to: {waapi_port}")
    client = WaapiClient(waapi_port)
    return client


def get_clipboard_content() -> Optional[List[str]]:
    """Return clipboard text as a list of lines.

    Returns ``None`` when the clipboard is empty or does not contain textual
    data.  ``pyperclip`` is tolerant and will return an empty string if it
    cannot determine the clipboard contents, which is why we perform the truthy
    check before splitting.
    """

    content = pyperclip.paste()
    if content:
        return content.strip().split("\r\n")
    return None


def show_error_message(message: str) -> None:
    """Show an error dialog with ``message`` as its body."""

    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)
    root.destroy()


def show_success_message(message: str) -> None:
    """Display a standard informational dialog that indicates success."""

    messagebox.showinfo("Success", message)


def show_message(title: str, message: str) -> None:
    """Display a general informational dialog with a custom title."""

    messagebox.showinfo(title, message)

### Returns a list with each selected object, its GUID, name and any additional arguments
def get_selected_items(
    client: WaapiClient, *additional_fields: str
) -> Optional[List[Dict[str, Any]]]:
    """Return metadata for the currently selected Wwise objects.

    Parameters
    ----------
    client:
        The WAAPI client used to perform the ``ak.wwise.ui.getSelectedObjects``
        call.
    *additional_fields:
        Optional WAAPI property names that should be returned for each object in
        addition to ``id`` and ``name``.

    Returns
    -------
    list of dict or ``None``
        A list containing the selected Wwise objects with the requested
        metadata, or ``None`` when no selection exists.
    """

    return_args = ["id", "name"]
    if additional_fields:
        return_args.extend(additional_fields)
    args = {"options": {"return": return_args}}
    result = client.call("ak.wwise.ui.getSelectedObjects", args)
    selected_items: List[Dict[str, Any]] = []
    if result:
        for obj in result["objects"]:
            selected_items.append(obj)
        return selected_items
    return None


def ask_user_input_num(
    title: str = "Input", message: str = "Insert the number of copies"
) -> Optional[int]:
    """Ask the user for an integer value via a Tkinter dialog."""

    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    number_of_copies = simpledialog.askinteger(
        title, message, parent=root, minvalue=1
    )
    root.destroy()
    return number_of_copies


def ask_user_input_str(
    title: str = "Input", message: str = "Enter the new name"
) -> Optional[str]:
    """Ask the user for a string value via a Tkinter dialog."""

    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    number_of_copies = simpledialog.askstring(title, message)
    root.destroy()
    return number_of_copies


def execute_func_times(func: Callable[[], None], times: int) -> None:
    """Execute ``func`` ``times`` times."""

    for _ in range(times):
        func()
