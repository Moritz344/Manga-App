import customtkinter as ctk
import tkinter as tk
from handling_requests import get_manga_title,get_manga_chapters,get_server_data,downloading_chapters
from handling_requests import search_manga_result
import requests

window = ctk.CTk()
window.geometry("800x600")

manga_title = None


def test_frame(window,manga_title):
    def get_title():
        manga_title = search_field.get()
        CollectMangaInfos(manga_title)
    def get_manga_with_name():
        manga_title = search_field.get()
        print(manga_title)
        c = DisplayMangaInfos(manga_title,main_frame)
        c.display_mangas()

    
    entry_frame = ctk.CTkFrame(window,width=1200,height=100,)
    entry_frame.pack(side="top",padx=0,pady=50)

    search_field = ctk.CTkEntry(entry_frame,width=900,height=70,font=(None,30))
    search_field.pack(side="top",padx=0,pady=10)

    download_btn = ctk.CTkButton(entry_frame,text="Download",font=(None,20),command=get_title)
    download_btn.pack(side="top")

    search_btn = ctk.CTkButton(entry_frame,text="Search",font=(None,20),command=get_manga_with_name)
    search_btn.pack(side="top",padx=0,pady=0)


    main_frame = ctk.CTkFrame(window,width=1000,height=800,fg_color="transparent")
    main_frame.pack(side="top",padx=0,pady=10,expand=True)
    

    return manga_title

manga_title = test_frame(window,manga_title)


class DisplayMangaInfos(object):
    def __init__(self,manga_title,window):
        self.manga_title = manga_title
        self.window = window
        #self.result = search_manga_result(manga_title)

        #self.manga_num = len(self.result)

    def display_mangas(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        grid_container = ctk.CTkFrame(self.window, width=1000, height=800,fg_color="transparent")
        grid_container.grid(row=0, column=0, padx=20, pady=20)
        grid_container.grid_propagate(False)  

        scrollable_frame = ctk.CTkScrollableFrame(master=grid_container, width=1000, height=500)
        scrollable_frame.pack()

        for i in range(3):  # 3 Spalten
            grid_container.grid_columnconfigure(i, weight=1)
        for i in range(3):  # 3 Zeilen
            grid_container.grid_rowconfigure(i, weight=1)

        for i in range(10):
            row = i // 1
            col = i % 1

            block = ctk.CTkFrame(scrollable_frame,width=1000,height=200)
            block.grid(row=row,column=col,padx=20,pady=20)


            block_label = ctk.CTkLabel(block,text=f"{i}",font=(None,30))#text=f"{self.result[i]}",font=(None,15))
            block_label.place(x=0,y=0)


class CollectMangaInfos(object):
    def __init__(self,manga_title):
        try:
            manga_id = get_manga_title(manga_title)
            chapter_id,chapter_number,chapter_1_id,chapter_1_num = get_manga_chapters(manga_id)
            pages,host,chapter_hash = get_server_data(chapter_id)
            downloading_chapters(pages,chapter_1_num,manga_title,host,chapter_hash)
        except Exception as e:
            print(e)


window.mainloop()
