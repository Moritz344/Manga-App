import customtkinter as ctk
import tkinter as tk
from handling_requests import get_manga_title
import requests

window = ctk.CTk()
window.geometry("800x600")

manga_title = None


def test_frame(window,manga_title):
    def get_title():
        manga_title = search_field.get()
        CollectMangaInfos(manga_title)

    
    entry_frame = ctk.CTkFrame(window,width=1200,height=100,)
    entry_frame.pack(side="top",padx=0,pady=50)

    search_field = ctk.CTkEntry(entry_frame,width=900,height=70,font=(None,30))
    search_field.pack(side="top",padx=0,pady=10)

    search_btn = ctk.CTkButton(entry_frame,text="Search",font=(None,20),command=get_title)
    search_btn.pack(side="top")


    t = ctk.CTkFrame(window,width=1000,height=800)
    t.pack(side="top",padx=0,pady=10)
    

    return manga_title

manga_title = test_frame(window,manga_title)

class CollectMangaInfos(object):
    def __init__(self,manga_title):
        manga_id = get_manga_title(manga_title)
window.mainloop()
