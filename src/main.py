import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame

#TODO: bug bei readmangascreen wenn ich zu dem search screen gehe
#TODO: json datei benutzen für settings
#TODO: mangas speichern in sql lite
#TODO: ChapterView ui verbessern siehe figma
#TODO: Downloaded Manga Page -> Wo man seine heruntergeladenen Mangas anschauen kann also history oder so
#TODO: Markierte Mangas Manga Page
#TODO: hacker theme 



window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
manga_title = None


manga_title = main_window_frame(window,manga_title)

window.mainloop()




