import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,start_main_screen_in_thread
from json_utils.settings import background
from session_name import *
from utils.ctkloader import CTkLoader
import threading

#TODO: manga covers parrallel im thread laden
#TODO: mangas speichern in sql lite
#TODO: history tab
#TODO: Readmangascreen tab verbessern
#TODO: colorschemes hinzufügen


window_title = choose_session_name()

window = ctk.CTk()
window.geometry("800x600")
window.title(window_title)
ctk.set_appearance_mode("dark")
window.configure(fg_color=f"{background}")

start_main_screen_in_thread(window,manga_title)


loader = CTkLoader(master=window,opacity=10,)
window.after(5000,loader.stop_loader)

window.mainloop()




