import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame
from settings import *
from session_name import *

#TODO: mangas speichern in sql lite
#TODO: history tab
#TODO: github tab
#TODO: Readmangascreen tab verbessern
#TODO: colorschemes hinzufügen


window_title = choose_session_name()

window = ctk.CTk()
window.geometry("800x600")
window.title(window_title)
ctk.set_appearance_mode("dark")
window.configure(fg_color=f"{background}")


main_window_frame(window,manga_title)



window.mainloop()




