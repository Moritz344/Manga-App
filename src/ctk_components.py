"""
ctk_components Module
--------------------

This module contains the implementation of various customtkinter components.
These components are designed to provide additional functionality and a modern look to your customtkinter applications.

Classes:
--------
- CTkAlert
- CTkBanner
- CTkNotification
- CTkCard
- CTkCarousel
- CTkInput
- CTkLoader
- CTkPopupMenu
- CTkProgressPopup
- CTkTreeview

Each class corresponds to a unique widget that can be used in your customtkinter application.

Author: rudymohammadbali (https://github.com/rudymohammadbali)
Date: 2024/02/26
Version: 20240226
"""

import io
import os
import sys
from tkinter import ttk

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

import customtkinter as ctk
from PIL import Image


class CTkGif(ctk.CTkLabel):

    def __init__(self, master: any, path, loop=True, acceleration=1, repeat=1, width=40, height=40, **kwargs):
        super().__init__(master, **kwargs)
        if acceleration <= 0:
            raise ValueError('Acceleration must be strictly positive')
        self.master = master
        self.repeat = repeat
        self.configure(text='')
        self.path = path
        self.count = 0
        self.loop = loop
        self.acceleration = acceleration
        self.index = 0
        self.is_playing = False
        self.gif = Image.open(path)
        self.n_frame = self.gif.n_frames
        self.frame_duration = self.gif.info['duration'] * 1 / self.acceleration
        self.force_stop = False

        self.width = width
        self.height = height

    def update(self):
        if self.index < self.n_frame:
            if not self.force_stop:
                self.gif.seek(self.index)
                self.configure(image=ctk.CTkImage(self.gif, size=(self.width, self.height)))
                self.index += 1
                self.after(int(self.frame_duration), self.update)
            else:
                self.force_stop = False
        else:
            self.index = 0
            self.count += 1
            if self.is_playing and (self.count < self.repeat or self.loop):
                self.after(int(self.frame_duration), self.update)
            else:
                self.is_playing = False

    def start(self):
        if not self.is_playing:
            self.count = 0
            self.is_playing = True
            self.after(int(self.frame_duration), self.update)

    def stop(self, forced=False):
        if self.is_playing:
            self.is_playing = False
            self.force_stop = forced

    def toggle(self, forced=False):
        if self.is_playing:
            self.stop(forced=forced)
        else:
            self.start()


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ICON_DIR = os.path.join(CURRENT_PATH, "assets", "icons")

ICON_PATH = {
    "close": (os.path.join(ICON_DIR, "close_black.png"), os.path.join(ICON_DIR, "close_white.png")),
    "images": list(os.path.join(ICON_DIR, f"image{i}.jpg") for i in range(1, 4)),
    "eye1": (os.path.join(ICON_DIR, "eye1_black.png"), os.path.join(ICON_DIR, "eye1_white.png")),
    "eye2": (os.path.join(ICON_DIR, "eye2_black.png"), os.path.join(ICON_DIR, "eye2_white.png")),
    "info": os.path.join(ICON_DIR, "info.png"),
    "warning": os.path.join(ICON_DIR, "warning.png"),
    "error": os.path.join(ICON_DIR, "error.png"),
    "left": os.path.join(ICON_DIR, "left.png"),
    "right": os.path.join(ICON_DIR, "right.png"),
    "warning2": os.path.join(ICON_DIR, "warning2.png"),
    "loader": os.path.join(ICON_DIR, "loader.gif"),
    "icon": os.path.join(ICON_DIR, "icon.png"),
    "arrow": os.path.join(ICON_DIR, "arrow.png"),
    "image": os.path.join(ICON_DIR, "image.png"),
}

class CTkLoader(ctk.CTkFrame):
    def __init__(self, master: any, opacity: float = 0.8, width: int = 40, height: int = 40):
        self.master = master
        self.master.update()
        self.master_width = self.master.winfo_width()
        self.master_height = self.master.winfo_height()
        super().__init__(master, width=self.master_width, height=self.master_height, corner_radius=0)

        #set_opacity(self.winfo_id(), value=opacity)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loader = CTkGif(self, ICON_PATH["loader"], width=width, height=height)
        self.loader.grid(row=0, column=0, sticky="nsew")
        self.loader.start()

        self.place(relwidth=1.0, relheight=1.0)

    def stop_loader(self):
        self.loader.stop()
        self.destroy()

