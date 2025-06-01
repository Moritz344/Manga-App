import customtkinter as ctk
import tkinter as tk
from handling_requests import *
import requests
import os
from PIL import Image
from display_manga import DisplayMangaInfos,ReadMangaScreen,main_window_frame

#TODO: mangas speichern in sql lite
#TODO: ui readmanga screen verbessern = bug fixen mit button verschwindet
#TODO: ChapterView ui verbessern siehe figma

window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
manga_title = None



manga_title = main_window_frame(window,manga_title)

window.mainloop()




