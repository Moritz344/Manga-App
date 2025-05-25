import customtkinter as ctk
import tkinter as tk
from handling_requests import get_manga_title,get_manga_chapters,get_server_data,downloading_chapters
from handling_requests import search_manga_result
import requests
import os

window = ctk.CTk()
window.geometry("800x600")
ctk.set_appearance_mode("dark")
manga_title = None


def main_window_frame(window,manga_title):
    def get_manga_with_name():
        manga_title = search_field.get()
        print(manga_title)
        c = DisplayMangaInfos(manga_title,main_frame,search_field,search_btn,entry_frame)
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
    def __init__(self,manga_title,window,search_field,search_btn,entry_frame):
        self.manga_title = manga_title
        self.window = window
        self.result = search_manga_result(manga_title)

        self.search_field = search_field
        self.search_btn = search_btn
        self.entry_frame = entry_frame

        self.manga_num = len(self.result)

    def read_btn(self,r,):
        folder_path = f"Mangadex/{r}"
        if os.path.exists(folder_path):
            print("Ready to read:",r)
            for widget in self.window.winfo_children():
                widget.destroy()
            self.search_field.pack_forget()
            self.search_btn.pack_forget()
            self.entry_frame.pack_forget()
            
            ReadMangaScreen(r,self.window)
        else:
            print("Download the Manga first! ")

    def download_manga(self,m):
        print(m)
        x = CollectMangaInfos(m)
        x.download_manga()
        
    def display_mangas(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        grid_container = ctk.CTkFrame(self.window, width=1000, height=800,fg_color="transparent")
        grid_container.grid(row=0, column=0, padx=20, pady=20)
        grid_container.grid_propagate(False)  

        scrollable_frame = ctk.CTkScrollableFrame(master=grid_container, width=1000, height=900)
        scrollable_frame.pack()

        for i in range(3):  # 3 Spalten
            grid_container.grid_columnconfigure(i, weight=1)
        for i in range(3):  # 3 Zeilen
            grid_container.grid_rowconfigure(i, weight=1)

        for i in range(self.manga_num):
            row = i // 1
            col = i % 1

            block = ctk.CTkFrame(scrollable_frame,width=950,height=150,
            border_width=3,border_color="white")

            block.grid(row=row,column=col ,padx=20,pady=10)


            block_label = ctk.CTkLabel(block,text=f"{self.result[i]}",font=(None,30))
            block_label.place(x=20,y=10)

            # description label
            curr_manga = block_label.cget("text")

            block_button = ctk.CTkButton(block,text="Read",font=(None,30),command= lambda r=curr_manga: self.read_btn(r))
            block_button.place(x=20,y=80)

            download_button = ctk.CTkButton(block,text="Download",font=(None,30),command= lambda m=curr_manga: self.download_manga(m))  # <-- WAIT THAT WORKED? LAMBDA THE GOAT
            download_button.place(x=200,y=80)

class ReadMangaScreen(object):
    def __init__(self,manga_title,window):
        self.manga_title = manga_title
        self.window = window
        self.manga_path = f"Mangadex/{manga_title}"
        self.chapter_number = 0

        self.back_btn = ctk.CTkButton(self.window,text="Back",font=(None,30),command= lambda: self.search_screen())
        self.back_btn.pack()

        self.manga_title_label = ctk.CTkLabel(self.window,text=f"{self.manga_title}",font=(None,30))
        self.manga_title_label.pack()

        self.chapter_label = ctk.CTkLabel(self.window,text=f"Chapter: {self.chapter_number}",font=(None,30))
        self.chapter_label.pack()

        self.get_manga_information()

    def clear_ui_elements(self):
        self.back_btn.pack_forget()
        self.manga_title_label.pack_forget()
        self.chapter_label.pack_forget()

    def search_screen(self):
        self.clear_ui_elements()
        main_window_frame(self.window,self.manga_title)

    def get_manga_information(self):
        manga_id = get_manga_title(self.manga_title)
        
        chapter_list = os.listdir(self.manga_path)
        for i,chapter in enumerate(chapter_list):
            print(i,chapter)
            self.chapter_number = i
        self.chapter_label.configure(text=f"Chapter (Downloaded): {self.chapter_number}")
        
        #chapters = get_manga_chapters(manga_id)
        #for chapter_id,chapter_number in chapters:
        #    result = get_server_data(chapter_id)
        #    if result is None:
        #        return
        #    pages,host,chapter_hash = result

        #    print(chapter_number)




class CollectMangaInfos(object):
    def __init__(self,manga_title):
                print()
                manga_id = get_manga_title(manga_title)
                print()
                self.chapters = get_manga_chapters(manga_id)
                print(self.chapters)
                self.manga_id = manga_id
                self.manga_title = manga_title
    def download_manga(self):
                for chapter_id,chapter_number in self.chapters:
                    result = get_server_data(chapter_id)
                    if result is None:
                        return
                    pages,host,chapter_hash = result

                    downloading_chapters(pages,chapter_number,self.manga_title,host,chapter_hash)

                    print("id,num",chapter_id,chapter_number)
                    print("pages,host,hash",pages,host,chapter_hash)
                    print("Manga id",self.manga_id)


window.mainloop()
