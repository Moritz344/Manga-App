import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame

#TODO: Ordne mit grid an
#TODO: mangas speichern in sql lite
#TODO: ui readmanga screen verbessern = bug fixen mit button verschwindet
#TODO: ChapterView ui verbessern siehe figma
#TODO: Downloaded Manga Page -> Wo man seine heruntergeladenen Mangas anschauen kann also history oder so
#TODO: Markierte Mangas Manga Page

#TODO: ich bin so cooked. Nach einer Woche kann ich das hier nicht mehr lesen bro.


window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
manga_title = None


manga_title = main_window_frame(window,manga_title)

window.mainloop()




