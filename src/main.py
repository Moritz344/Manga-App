import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame
from settings import *

#TODO: manga in scrollableframe?
#TODO: mark mangas as downloaded
#TODO: mangas speichern in sql lite
#TODO: history page
#TODO: Markierte Mangas Manga Page



window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
window.configure(fg_color=f"{background}")


main_window_frame(window,manga_title)



window.mainloop()




