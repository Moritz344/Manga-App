import customtkinter as ctk
from handling_requests import *
from PIL import Image
from tkinter import *
import tkinter.font as tkFont

def main_window_frame(window,manga_title):
    def get_manga_with_name():
        manga_title = search_field.get()
        print(manga_title)
        c = DisplayMangaInfos(manga_title,main_frame,search_field,search_btn,entry_frame)
        c.display_mangas()


    entry_frame = ctk.CTkFrame(window,width=2000,height=500,fg_color="transparent")
    entry_frame.pack(side="top",padx=0,pady=10)

    search_btn = ctk.CTkButton(entry_frame,text="Search",height=70,font=(None,30),fg_color="#7D7D7D",command=lambda :get_manga_with_name(),
    )
    search_btn.pack(side="left",padx=10,pady=10)



    search_field = ctk.CTkEntry(entry_frame,width=1300,height=70,font=(None,30),placeholder_text="Search Manga ...",placeholder_text_color="#B3B3B3")
    search_field.pack(side="top",padx=0,pady=10)




    main_frame = ctk.CTkFrame(window,width=2000,height=2000,fg_color="transparent")
    main_frame.pack(side="top",anchor="n",padx=0,pady=10,expand=True)

    c = DisplayMangaInfos("naruto",main_frame,search_field,search_btn,entry_frame)
    c.display_mangas()

    return manga_title

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



class ReadMangaScreen(object):
    def __init__(self,manga_title,window):
        self.manga_title = manga_title
        self.window = window
        self.manga_path = f"Mangadex/{manga_title}"


        self.chapter_number = 0

        self.current_chapter_number = 0
        self.page_number: int = 0
        self.pages_len = 50
        self.current_page_number: int = 0
        self.pages_list = []

        self.back_btn = ctk.CTkButton(self.window,text="Back",font=(None,30),command= lambda: self.search_screen())
        self.back_btn.pack()

        self.manga_title_label = ctk.CTkLabel(self.window,text=f"{self.manga_title}",font=(None,30))
        self.manga_title_label.pack()

        self.chapter_label = ctk.CTkLabel(self.window,text=f"Chapter: {self.chapter_number}",font=(None,30))
        self.chapter_label.pack()

        self.manga_field = ctk.CTkFrame(self.window,width=1000,height=800)
        self.manga_field.pack()

        self.next_page_btn = ctk.CTkButton(self.window,text="Next Page",command=self.next_page)
        self.next_page_btn.pack()

        self.prev_page_btn = ctk.CTkButton(self.window,text="Previous Page",command=self.prev_page)
        self.prev_page_btn.pack()

        self.next_chapter_btn = ctk.CTkButton(self.window,text="Next Chapter",command=self.next_chapter)
        self.next_chapter_btn.place(x=0,y=50)
        self.prev_chapter_btn = ctk.CTkButton(self.window,text="Previous Chapter",command=self.prev_chapter)
        self.prev_chapter_btn.place(x=0,y=0)

        self.current_page = ctk.CTkLabel(self.window,text=f"Page:{self.current_page_number}")
        self.current_page.pack()

        self.current_chapter = ctk.CTkLabel(self.window,text="Chapter:{self.current_chapter}")

        try:
            self.manga_page_image = ctk.CTkImage(
            Image.open(f"{self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")
            ,size=(1000,800))
        except Exception as e:
            print(e)

        self.manga_image_label = ctk.CTkLabel(self.manga_field,text="",image=self.manga_page_image)
        self.manga_image_label.pack()

        self.get_manga_information()

    def next_chapter(self):
            print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number <= self.chapter_number - 1:
                self.current_page_number = 0
                self.current_chapter_number += 1
                self.update_image(self.current_page_number,self.current_chapter_number)
                self.manga_image_label.configure(image=self.manga_page_image)
                self.update_pages_counter(self.current_chapter_number )
    def prev_chapter(self):
            print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number > 0:
                self.current_page_number = 0
                self.current_chapter_number -= 1
                self.update_image(self.current_page_number,self.current_chapter_number)
                self.manga_image_label.configure(image=self.manga_page_image)
                self.update_pages_counter(self.current_chapter_number )

    def update_pages_counter(self,chapter_count):
        try:
            page_list = os.listdir(f"{self.manga_path}/Chapter_{chapter_count}")
            self.pages_len = len(page_list)
            self.current_page.configure(text=f"Page:{self.current_page_number} / {self.pages_len}")
        except Exception as e:
            print(e)


    def update_image(self,page,chapter):
        try:
            self.manga_page_image = ctk.CTkImage(
            Image.open(f"{self.manga_path}/Chapter_{chapter}/Page_{page}")
            ,size=(1000,800))
        except Exception as e:
            print(e)

    def get_pages_chapters(self):
        chapter_list = os.listdir(self.manga_path)
        self.current_chapter_number = len(chapter_list ) -2
        self.chapter_number = len(chapter_list)

            #print(page_list)

        self.chapter_label.configure(text=f"Chapter (Downloaded): {self.chapter_number}")

    def next_page(self):
        if self.current_page_number <= self.pages_len - 1:
            self.current_page_number += 1
            self.update_image(self.current_page_number,self.current_chapter_number)

            self.update_pages_counter(self.current_chapter_number)

            self.manga_image_label.configure(image=self.manga_page_image)
        elif self.current_page_number > self.pages_len:
            self.current_page_number = 0
            self.current_chapter_number += 1
            self.update_image(self.current_page_number,self.current_chapter_number)

            self.update_pages_counter(self.current_chapter_number)

            self.manga_image_label.configure(image=self.manga_page_image)
            print(f"Next chapter: {self.current_chapter_number}")

    def prev_page(self):
        if self.current_page_number > 0:
            self.current_page_number -= 1

            self.update_image(self.current_page_number,self.current_chapter_number)
            self.manga_image_label.configure(image=self.manga_page_image)
            self.update_pages_counter(self.current_chapter_number)

    def clear_ui_elements(self):
        self.back_btn.pack_forget()
        self.manga_title_label.pack_forget()
        self.chapter_label.pack_forget()

        self.current_chapter.pack_forget()
        self.current_page.pack_forget()
        self.prev_page_btn.pack_forget()
        self.next_page_btn.pack_forget()
        self.manga_image_label.pack_forget()
        self.manga_field.pack_forget()
        self.prev_chapter_btn.place_forget()
        self.next_chapter_btn.place_forget()

    def search_screen(self):
        self.clear_ui_elements()
        main_window_frame(self.window,self.manga_title)

    def get_manga_information(self):
        manga_id = get_manga_title(self.manga_title)


        self.get_pages_chapters()



class DisplayMangaInfos(object):
    def __init__(self,manga_title,window,search_field,search_btn,entry_frame):
        self.manga_title = manga_title
        self.window = window
        self.result = search_manga_result(manga_title)


        
        self.manga_list = []
        
        # This is slow
        self.covers = []

        #for manga in self.result:
        #        manga_id,fileName = get_manga_cover(manga)
        #        self.manga_list.append((manga_id))
        #        self.manga_list.append((fileName))
        #        image_cover = load_cover_image(manga_id,fileName)
        #        self.covers.append(image_cover)

        manga_id,fileName = get_manga_cover(manga_title)
        image_cover = load_cover_image(manga_id,fileName)
        
        self.image_cover = image_cover
        print(self.covers)

        self.search_field = search_field
        self.search_btn = search_btn
        self.entry_frame = entry_frame

        self.max_manga_num = 8
        self.manga_num = self.max_manga_num#len(self.result)

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
    def open_manga(self,r):
        print(r)
    def display_mangas(self):
        

        for widget in self.window.winfo_children():
            widget.destroy()


        #grid_container = ctk.CTkFrame(self.window, width=1500, height=1080,fg_color="transparent")
        #grid_container.grid(row=0, column=0, padx=20, pady=20)
        #grid_container.grid_propagate(False)
        #grid_container.columnconfigure(1,weight=1)

        grid_container = ctk.CTkFrame(self.window,width=1500,height=1100,fg_color="transparent")
        grid_container.pack(padx=10,pady=10)


        scrollable_frame = ctk.CTkScrollableFrame(master=grid_container, width=1500,height=800, fg_color="#272727")
        scrollable_frame.grid()
        



        for i in range(self.manga_num):

            row = i // 3
            col = i % 3

            block = ctk.CTkFrame(scrollable_frame,width=350,height=350,fg_color="transparent",corner_radius=0)
            block.grid(row=row,column=col ,padx=75,pady=50)

            text_block = ctk.CTkFrame(scrollable_frame,width=400,height=100,fg_color="transparent",corner_radius=0)
            text_block.grid(row=row,column=col,padx=28,pady=0,sticky="se")



            block_label = ctk.CTkLabel(text_block,text=f"{self.result[i]}",compound="left",font=(None,20,"bold"),text_color="white",
            fg_color="transparent")
            block_label.place(x=5,y=0)

            block_image = ctk.CTkLabel(block,text=f"",image=self.image_cover,)
            block_image.place(x=0,y=0)


            # description label
            curr_manga = block_label.cget("text")


            open_btn = ctk.CTkButton(text_block,text="Open",fg_color="#7D7D7D",font=(None,20),command= lambda r=curr_manga: self.open_manga(r))
            open_btn.place(x=5,y=50)


            #block_button = ctk.CTkButton(grid_container,text="Read",font=(None,30),command= lambda r=curr_manga: self.read_btn(r))
            #block_button.grid(row=row,column=col,padx=90,pady=0,sticky="se")

            #download_button = ctk.CTkButton(grid_container,text="Download",font=(None,30),command= lambda m=curr_manga: self.download_manga(m))
            #download_button.grid(row=row,column=col,padx=90,pady=0,sticky="sw")


