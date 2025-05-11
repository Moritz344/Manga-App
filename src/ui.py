import customtkinter as ctk
import tkinter as tk
from handling_requests import get_manga_title,get_manga_chapters,get_server_data,downloading_chapters
from handling_requests import search_manga_result
import requests

window = ctk.CTk()
window.geometry("800x600")

manga_title = None


def main_window_frame(window,manga_title):
    def get_manga_with_name():
        manga_title = search_field.get()
        print(manga_title)
        c = DisplayMangaInfos(manga_title,main_frame)
        c.display_mangas()

    
    entry_frame = ctk.CTkFrame(window,width=1200,height=100,fg_color="transparent")
    entry_frame.pack(side="top",padx=0,pady=10)

    search_btn = ctk.CTkButton(entry_frame,text="Search",height=70,font=(None,30),command=get_manga_with_name)
    search_btn.pack(side="left",padx=10,pady=10)


    search_field = ctk.CTkEntry(entry_frame,width=900,height=70,font=(None,30))
    search_field.pack(side="top",padx=0,pady=10)




    main_frame = ctk.CTkFrame(window,width=2000,height=2000,fg_color="transparent")
    main_frame.pack(side="top",anchor="n",padx=0,pady=10,expand=True)
    

    return manga_title

manga_title = main_window_frame(window,manga_title)


class DisplayMangaInfos(object):
    def __init__(self,manga_title,window):
        self.manga_title = manga_title
        self.window = window
        self.result = search_manga_result(manga_title)

        self.manga_num = len(self.result)

    def read_btn(self):
        print("button")

    def download_manga(self,m):
        print(m)
    def display_mangas(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        grid_container = ctk.CTkFrame(self.window, width=1000, height=800,fg_color="transparent")
        grid_container.grid(row=0, column=0, padx=20, pady=20)
        grid_container.grid_propagate(False)  

        scrollable_frame = ctk.CTkScrollableFrame(master=grid_container, width=1000, height=1000)
        scrollable_frame.pack()

        for i in range(3):  # 3 Spalten
            grid_container.grid_columnconfigure(i, weight=1)
        for i in range(3):  # 3 Zeilen
            grid_container.grid_rowconfigure(i, weight=1)

        for i in range(10):
            row = i // 1
            col = i % 1

            block = ctk.CTkFrame(scrollable_frame,width=950,height=150,
            border_width=3,border_color="white")
            block.grid(row=row,column=col,padx=20,pady=20)


            block_label = ctk.CTkLabel(block,text=f"{self.result[i]}",font=(None,30))
            block_label.place(x=20,y=10)

            # description label

            block_button = ctk.CTkButton(block,text="Read",font=(None,30),command=self.read_btn)
            block_button.place(x=20,y=80)
            
            curr_manga = block_label.cget("text")

            download_button = ctk.CTkButton(block,text="Download",font=(None,30),command= lambda m=curr_manga: self.download_manga(m))  # <-- WAIT THAT WORKED? LAMBDA THE GOAT
            download_button.place(x=200,y=80)

class ReadMangaScreen(object):
    def __init__(self,manga_title,pages):
        pass



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
