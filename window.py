"""
The window module is what contains the window of the program

Copyright (C) 2023 - Ziad Ahmed (Mr.X)
"""
from cefpython3 import cefpython as cef
import ctypes
import tkinter as tk
import sys
import os
import platform
import logging as _logging

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"
from tkinter import *
from tkinter import ttk
import constants
import webview


class AppWindow(Tk):
    def __init__(self) -> None:
        """
        This class represents the App's Main Window
        """
        super().__init__()
        self.title(constants.WINDOW_TITLE)
        self.geometry(f"{constants.WINDOW_MIN_WIDTH}x{constants.WINDOW_MIN_HEIGHT}")
        self.minsize(constants.WINDOW_MIN_WIDTH, constants.WINDOW_MIN_HEIGHT)
        self.resizable(True, True)
        self.webview_widget = webview.BrowserFrame(self, navigation_bar=None)
        self.webview_widget.pack(fill=BOTH, expand=YES)
        self.bind("<Configure>", self.on_configure)

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.webview_widget:
            self.webview_widget.on_root_configure()
    
    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.webview_widget:
            width = event.width
            height = event.height
            try:
                if self.navigation_bar:
                    height = height - self.navigation_bar.winfo_height()
            except Exception as _err:
                print("[ERROR]: It appears that this window doesn't have a navigation bar associated with it\nError details are: {_err}".format(_err=_err))
            self.webview_widget.on_mainframe_configure(width, height)
        





if __name__ == '__main__':
    logger.setLevel(_logging.DEBUG)
    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info("CEF Python {ver}".format(ver=cef.__version__))
    logger.info("Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    app = AppWindow()
    settings = {}
    if MAC:
        settings["external_message_pump"] = True
    cef.Initialize(settings=settings)
    app.mainloop()
    logger.debug("Main loop exited")
    cef.Shutdown()