import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame
from ctk_components import CTkLoader
from settings import *

#TODO: chapterview -> scrollableframe -> scrollable für linux machen
#TODO: mark mangas as downloaded
#TODO: manga status
#TODO: json datei benutzen für settings
#TODO: mangas speichern in sql lite
#TODO: Downloaded Manga Page -> Wo man seine heruntergeladenen Mangas anschauen kann also history oder so
#TODO: Markierte Mangas Manga Page
#TODO: hacker theme 



window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
window.configure(fg_color=f"{graphite}")


main_window_frame(window,manga_title)
#loader = CTkLoader(master=window, opacity=0.8, width=40, height=40)
#window.after(500, loader.stop_loader) 



window.mainloop()




