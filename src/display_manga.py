import customtkinter as ctk
from handling_requests import *
from PIL import Image
import tkinter.font as tkFont
from settings import *
from ctk_components import CTkLoader
from write_to_json import write_data_to_json
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import random
import shutil

is_Downloaded = False


def main_window_frame(window,manga_title):
    def get_manga_with_name():
        window.focus()
        manga_title = search_field.get()
        print(manga_title)
        c.update_manga(manga_title)

    
    window.grid_rowconfigure(0, weight=0)  # settings_frame
    window.grid_rowconfigure(1, weight=0)  # entry_frame
    window.grid_rowconfigure(2, weight=1)  # main_frame fills remaining space
    window.grid_columnconfigure(0, weight=1)

    


    settings_frame = ctk.CTkFrame(window,width=1800,height=50,fg_color="transparent")

    entry_frame = ctk.CTkFrame(window,width=2000,height=500,fg_color="transparent")

    settings_btn = ctk.CTkButton(
    settings_frame,
    text="Settings",
    fg_color="transparent",
    text_color="white",
    hover_color=f"{button_hover_color}",
    font=(None,30))

    github_btn = ctk.CTkButton(
    settings_frame,
    text="Github",
    text_color="white",
    fg_color="transparent",
    hover_color=f"{button_hover_color}",
    font=(None,30))

    history_btn = ctk.CTkButton(
    settings_frame,
    text="History",
    text_color="white",
    fg_color="transparent",
    hover_color=f"{button_hover_color}",
    font=(None,30))

    kofgio= ctk.CTkButton(
    settings_frame,
    text="History",
    text_color="white",
    fg_color="transparent",
    hover_color=f"{button_hover_color}",
    font=(None,30))

    search_field = ctk.CTkEntry(entry_frame,
    width=1300,
    height=70,
    font=(None,30),
    placeholder_text="Search Manga ...",
    placeholder_text_color="#B3B3B3",
    corner_radius=10)
    search_field.grid(row=0,column=1,padx=10,pady=0,sticky="ew")
    
    search_image = ctk.CTkImage(Image.open("assets/icons/search.png"),size=(50,50))

    search_btn = ctk.CTkButton(entry_frame,text="",height=70,font=(None,30),fg_color=f"{button_color}",
    command=lambda :get_manga_with_name(),hover_color=f"{button_hover_color}",
    image=search_image)
    search_btn.grid(row=0,column=0,padx=0,pady=0,)






    main_frame = ctk.CTkFrame(window,width=2000,height=2000,fg_color="transparent")

    settings_frame.grid(row=0,column=0,pady=10,)
    entry_frame.grid(row=1,column=0,pady=10,)
    main_frame.grid(row=2,column=0,padx=10,pady=0,sticky="nsew")

    settings_btn.place(x=185,y=0,)
    history_btn.place(x=400,y=0,)
    github_btn.place(x=615,y=0,)

    every_frame = [search_field,search_btn,entry_frame,settings_frame,settings_btn,history_btn]

    popular_manga = get_popular_manga()   
    # TODO Popular manga anzeigen:
    c = DisplayMangaInfos(None,main_frame,every_frame,popular_manga)
    c.show_popular_manga()

    def on_enter(event):
        get_manga_with_name()

    window.bind("<Return>",on_enter)

    return manga_title

class CollectMangaInfos(object):
    def __init__(self,manga_title,window):
                self.window = window
                print()
                manga_id = get_manga_title(manga_title)
                print()
                
                self.chapters= get_manga_chapters(manga_id)
                print(self.chapters)

                self.manga_id = manga_id
                self.manga_title = manga_title


    def download_manga(self):
        error = ""
        try:
                for chapter_id,chapter_number in self.chapters:
                    result = get_server_data(chapter_id)
                    if result is None:
                        return
                    pages,host,chapter_hash = result


                    downloading_chapters(pages,chapter_number,self.manga_title,host,chapter_hash)

                    print("id,num: ",chapter_id,chapter_number)
                    print("pages,host,hash",pages,host,chapter_hash)
                    print("Manga id",self.manga_id)
        except Exception as e:
            error = e
        return error

class ReadMangaScreen:
    def __init__(self,manga_title,window,chapter_start):

        self.manga_title = manga_title
        self.window = window

        self.manga_path = f"Mangadex/{manga_title}"
        self.chapter_start = chapter_start

        self.chapter_number = 0
        print("DEBUG",chapter_start)
        if self.chapter_start == "":
            self.current_chapter_number = 0
        else:
            self.current_chapter_number = chapter_start


        self.arrow_image_right = ctk.CTkImage(Image.open("assets/arrow_right.png"),size=(30,30))
        self.arrow_image_left = ctk.CTkImage(Image.open("assets/arrow_left.png"),size=(30,30))

        self.page_number: int = 0
        self.pages_len = 50
        self.current_page_number: int = 0
        self.pages_list = []

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=0)



        self.option_field_2 = ctk.CTkFrame(self.window,width=800,height=300,)
        self.option_field_2.grid(row=1, column=1, sticky="ew", padx=10, pady=10)


        self.option_field = ctk.CTkFrame(self.window,width=300,height=800,)
        self.option_field.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        #self.manga_title_label = ctk.CTkLabel(self.option_field,text=f"{self.manga_title}",font=(None,30))
        #self.manga_title_label.pack(padx=0,pady=0)

        self.back_button = ctk.CTkButton(self.option_field,text="Back",font=(None,30),
        command= lambda: self.search_screen(),fg_color=f"{button_color}",hover_color=f"{button_hover_color}")
        self.back_button.pack(side="bottom",anchor="s",padx=0,pady=10)
        self.chapter_label = ctk.CTkLabel(self.option_field,text=f"Chapter: {self.chapter_number}",font=(None,30))
        self.chapter_label.pack()

        self.manga_field = ctk.CTkFrame(self.window,width=1000,height=800)
        self.manga_field.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)



        self.next_page_btn = ctk.CTkButton(self.option_field_2,text="",image=self.arrow_image_right,
        command=self.next_page,fg_color=f"{button_color}",hover_color=f"{button_hover_color}")
        self.next_page_btn.pack(side="right",anchor="s",padx=0,pady=0)

        self.prev_page_btn = ctk.CTkButton(self.option_field_2,text="",command=self.prev_page,
        fg_color=f"{button_color}",hover_color=f"{button_hover_color}",image=self.arrow_image_left)
        self.prev_page_btn.pack(side="left",anchor="s",padx=0,pady=0)

        self.next_chapter_btn = ctk.CTkButton(self.option_field_2,text="Next Chapter",
        command=self.next_chapter,fg_color=f"{button_color}",hover_color=f"{button_hover_color}",font=(None,20))
        self.next_chapter_btn.pack()
        self.prev_chapter_btn = ctk.CTkButton(self.option_field_2,text="Prev Chapter",
        command=self.prev_chapter,fg_color=f"{button_color}",hover_color=f"{button_hover_color}",font=(None,20))
        self.prev_chapter_btn.pack()


        self.current_page = ctk.CTkLabel(self.option_field_2,text=f"Page:{self.current_page_number}",
        font=(None,30,"bold"))
        self.current_page.pack()


        try:

            self.manga_page_image = ctk.CTkImage(
            Image.open(f"{self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")
            ,size=(800,800))
            print(f"{self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")
        except Exception as e:
            print("Failed to load image",e)
            self.manga_page_image = None
        
        
        if self.manga_page_image:
            self.manga_image_label = ctk.CTkLabel(self.manga_field,text="",image=self.manga_page_image)
        else:
            self.manga_image_label = ctk.CTkLabel(self.manga_field,text="No Image Available",font=(None,20),text_color="red")

        self.manga_image_label.pack()

        self.get_manga_information()

    def reset_grid_config(self):
        for i in range(3):
            self.window.grid_columnconfigure(i,weight=0)
        for i in range(2):
            self.window.grid_rowconfigure(i,weight=0)

    def next_chapter(self):
            print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number <= self.chapter_number - 1:
                self.current_page_number = 0
                self.current_chapter_number += 1
                self.update_image(self.current_page_number,self.current_chapter_number)
                self.manga_image_label.configure(image=self.manga_page_image)
                self.update_pages_counter(self.current_chapter_number )
                write_data_to_json("user_var",f"{self.manga_title}",self.current_chapter_number)
    def prev_chapter(self):
            print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number > 0:
                self.current_page_number = 0
                self.current_chapter_number -= 1
                self.update_image(self.current_page_number,self.current_chapter_number)
                self.manga_image_label.configure(image=self.manga_page_image)
                self.update_pages_counter(self.current_chapter_number )
                write_data_to_json("user_var",f"{self.manga_title}",self.current_chapter_number)

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
            ,size=(800,800))
        except Exception as e:
            print(e)

    def get_pages_chapters(self):
        print(f"{self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")
        chapter_list = os.listdir(self.manga_path)
        #self.current_chapter_number = len(chapter_list ) -2
        self.chapter_number = len(chapter_list)

            #print(page_list)
        print(f"get_pages_chapters: {self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")

        self.chapter_label.configure(text=f"Chapter (Downloaded): {self.chapter_number}")

    def next_page(self):
        if self.current_page_number <= self.pages_len - 1:
            self.current_page_number += 1
            self.update_image(self.current_page_number,self.current_chapter_number)

            print(f"{self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")
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
        for w in self.window.winfo_children():
            w.destroy()
        #self.back_button.destroy()
        #self.manga_title_label.destroy()
        #self.chapter_label.destroy()
        #self.next_page_btn.destroy()
        #self.prev_page_btn.destroy()
        #self.option_field.destroy()
        #self.option_field_2.destroy()
        #self.current_chapter.destroy()
        #self.manga_field.destroy()

    def search_screen(self):
        self.clear_ui_elements()
        self.reset_grid_config()
        main_window_frame(self.window,self.manga_title)

    def get_manga_information(self):
        manga_id = get_manga_title(self.manga_title)


        self.get_pages_chapters()

class ChapterView:
    def __init__(self,manga_title,window):

        self.window = window
        self.path = f"Mangadex/{manga_title}"
        self.chapter_list = []
        self.curr_block = ""
        self.all_chapters = None
        self.description = None
        self.genres: list = None
        self.manga_status: str = None



        self.frame_1 = ctk.CTkFrame(window,width=800,height=1000,)
        self.frame_1.pack(side="left",expand=True,padx=0,pady=100,)

        self.cover_frame = ctk.CTkFrame(self.frame_1,width=600,height=400,fg_color="transparent")
        self.cover_frame.place(x=10,y=10,)

        self.info_frame = ctk.CTkFrame(self.frame_1,width=600,fg_color="transparent")
        self.info_frame.place(x=300,y=10)



        self.frame_0 = ctk.CTkFrame(window,width=400,height=1000,fg_color="transparent")
        self.frame_0.pack(side="right",expand=True,padx=0,pady=100,)

        self.manga_title: str = manga_title
        manga_id,filename = get_manga_cover(self.manga_title)

        image_cover = load_cover_image(manga_id,filename,250,300)
        
        self.cover_label = ctk.CTkLabel(self.cover_frame,text="",anchor="s",image=image_cover)
        self.cover_label.pack(side="left",padx=0,pady=0,anchor="ne")

        self.get_all_chapters()
        self.title_label = ctk.CTkLabel(self.info_frame,text=f"{self.manga_title}",font=(None,30))
        self.title_label.pack(anchor="w",padx=0,pady=0,)
        


        self.chapter_text= ctk.CTkLabel(self.info_frame,text=f"all chapters",font=(None,20),
        text_color=f"{button_hover_color}")
        self.chapter_text.pack(anchor="w",padx=0,pady=0,)

        self.chapter_label= ctk.CTkLabel(self.info_frame,text=f"{self.all_chapters}",font=(None,30,"bold"))
        self.chapter_label.pack(anchor="w",padx=0,pady=0,)
        
        self.genre_text = ctk.CTkLabel(self.info_frame,text=f"Genres",
        text_color=f"{button_hover_color}",font=(None,20))
        self.genre_text.pack(anchor="w",padx=0,pady=0,)

        self.genre_label = ctk.CTkLabel(self.info_frame,text=f"{self.genres}",font=(None,20))
        self.genre_label.pack(anchor="w",padx=0,pady=0)

        self.continue_btn = ctk.CTkButton(self.frame_1,text="Continue Reading",fg_color=f"{color_blue}",
        font=(None,30,),width=200,command=self.continue_manga)
        self.continue_btn.place(x=10,y=340,)

        if self.frame_1.winfo_exists():
            self.start_over = ctk.CTkButton(self.frame_1,text="Read From Start",fg_color=f"{color_green}",
            font=(None,30,),width=270,command=lambda: self.start_over_func(0))

        self.start_over.place(x=10,y=400,)

        self.description_text = ctk.CTkLabel(self.frame_1,text=f"Description",
        text_color=f"{button_hover_color}",font=(None,25))
        self.description_text.place(x=10,y=490,)
        

        
        self.desc_frame = ctk.CTkScrollableFrame(self.frame_1,width=500,height=200,)
        self.desc_frame.place(x=10,y=530)
        
        self.description_label = ctk.CTkLabel(self.desc_frame,text=f"{self.description}",font=(None,20),
        justify="left",wraplength=500)
        self.description_label.pack(side="left",padx=0,pady=0)
        
        
        self.chapter_frame = ctk.CTkScrollableFrame(self.frame_0,width=750,height=1000,fg_color="transparent")
        self.chapter_frame.pack(side="left",padx=10,pady=30,anchor="ne")




        self.combobox_var = ctk.StringVar(value="Start From First")
        self.order_chapter = ctk.CTkComboBox(self.frame_0,
        values=["Start From Last","Start From First"],state="readonly",variable=self.combobox_var,
                                             command=self.combobox_order)
        self.order_chapter.place(x=15,y=0)

        self.delete_btn = ctk.CTkButton(self.frame_1,text="Delete Manga",
        font=(None,20),fg_color="#e05033",hover_color=f"#a5250b",command=lambda: self.delete_manga(True))
        self.delete_btn.place(x=200,y=780)

       
        self.back_button = ctk.CTkButton(self.frame_1,text="Back",font=(None,20),fg_color=f"{button_color}",
                                             hover_color=f"{button_hover_color}",command=self.back_btn)
        self.back_button.place(x=10,y=780)

        
        self.manga_status_handler()
        
        self.manga_status_text_label = ctk.CTkLabel(self.info_frame,text="Manga Status",font=(None,20)
        ,text_color=f"{button_hover_color}")
        self.manga_status_text_label.pack(anchor="w",padx=0,pady=0)

        self.manga_status_label = ctk.CTkLabel(self.info_frame,text=f"{self.manga_status}",font=(None,20))
        self.manga_status_label.pack(anchor="w",padx=0,pady=0)

        self.get_description_len()
        self.get_chapters()
        self.combobox_order(self.combobox_var.get())
    
    def manga_status_handler(self):
        manga_id = get_manga_title(manga_title)
        manga_status = get_manga_status(manga_id)
        self.manga_status = manga_status


    def get_description_len(self):
        text = self.description_label.cget("text") 
        desc_len = len(text)
        print(desc_len)

    def delete_manga(self,show_message):
        try:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
                print(f"Successfully Removed: {self.path}")
                if show_message:
                    CTkMessagebox(
                    self.window,
                    title="Remove Manga",
                    message=f"Successfully Removed {self.manga_title}",
                    icon="cancel",justify="center")
                self.back_btn()
        except Exception as e:
            print(e)
    
    def combobox_order(self,v):
        if v == "Start From Last":
            self.display_chapter_list("last")
        elif v == "Start From First":
            self.display_chapter_list("start")
            
    def continue_manga(self):
        chapter_start = history
        self.clear_all_ui_elements()
        ReadMangaScreen(self.manga_title,self.window,chapter_start)

    def start_over_func(self,m):
        chapter_start = m
        self.clear_all_ui_elements()
        ReadMangaScreen(self.manga_title,self.window,chapter_start)

    def get_chapters(self) -> None:
        try:
            # get all downloaded chapters
            self.chapter_list = os.listdir(self.path)
        except FileNotFoundError :
            c = CollectMangaInfos(self.manga_title,self.window)
            error = c.download_manga()
        
    def get_all_chapters(self):
        try:
            manga_id = get_manga_title(self.manga_title)
            chapter_number= get_only_chapters(manga_id)
            self.all_chapters = chapter_number

            # get the description of the manga 
            description = get_manga_description(manga_id)
            self.description = description

            # get the genre of the manga 
            genre_list = get_manga_genre(manga_id)
            self.genres = genre_list
            self.genres = ",".join(self.genres)
        except Exception as e:
            CTkMessagebox(self.window,title="Error",
            message=f"No Chapter for {self.manga_title} found",
            icon="cancel")
            print("get_all_chapters:",e)

    
    def read_manga(self,m) -> None:
        try:
            chapter_start = m
            #write_data_to_json("user_var",f"{m}",chapter_start)
            print(f"DEBUG: Manga start is at chapter {m}")
            self.clear_all_ui_elements()
            ReadMangaScreen(self.manga_title,self.window,chapter_start)
            write_data_to_json("user_var",f"{self.manga_title}",m)
        except Exception as e:
            print(e)

    def update_chapter_list(self):
        for widget in self.chapter_frame.winfo_children():
            widget.destroy()
        

    def display_chapter_list(self,order):
        if order == "start":
            self.update_chapter_list()
            for i in range(len(self.chapter_list) ):
                
                block = ctk.CTkButton(self.chapter_frame,
                text=f"{i}  ",
                width=500,
                height=100,
                corner_radius=0,
                anchor="ne",
                font=(None,30,"bold"),fg_color=f"{block_color}",hover_color=f"{button_hover_color}",
                command= lambda m=self.curr_block: self.read_manga(m))

                block.pack(padx=0,pady=5,anchor="w")
                # get the current chapter the user wants to start at
                self.curr_block = i
        elif order == "last":
            self.update_chapter_list()
            chapter_len = len(self.chapter_list)
            for i in range(chapter_len-1,-1,-1):
                block = ctk.CTkButton(self.chapter_frame,
                text=f"{i}  ",
                width=500,
                height=100,
                corner_radius=0,
                anchor="ne",
                font=(None,30,"bold"),fg_color=f"{block_color}",hover_color=f"{button_hover_color}",
                command= lambda m=self.curr_block: self.read_manga(m))

                block.pack(padx=0,pady=5,anchor="w")
                # get the current chapter the user wants to start at
                self.curr_block = i - 1
                print("curr_block",self.curr_block)


    def clear_all_ui_elements(self):
        try:
            for w in self.window.winfo_children():
                w.destroy()

            #self.back_button.destroy()
            #self.chapter_label.destroy()
            #self.chapter_frame.destroy()
            #self.frame_0.destroy()
            #self.frame_1.destroy()
            #self.chapter_header.destroy()
            #self.combobox_order.destroy()
        except Exception as e:
            print(e)
    def back_btn(self):
        self.clear_all_ui_elements()
        main_window_frame(self.window,"Naruto")

class DisplayMangaInfos:
    def __init__(self,manga_title,window,main_frames,popular_manga):

        self.manga_title = manga_title
        self.window = window
        self.popular_manga = popular_manga
        self.main_frames = main_frames

        # ergebnis der mangas beim suchen
        self.result = search_manga_result(manga_title)

        
        self.frame_values = ["show popular manga","show random manga"]
        self.scrollable_frame_list = ctk.CTkComboBox(self.window,
        values=self.frame_values,width=160,height=50,
        command=self.switch_manga_list)
        #self.scrollable_frame_list.place(x=1730,y=0)


        self.grid_container = ctk.CTkFrame(self.window,width=1500,height=1100,fg_color="transparent")
        self.grid_container.pack(padx=10,pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.grid_container, 
        width=1500,height=840, fg_color="#272727")
        self.scrollable_frame.grid(row=2,column=0,sticky="nsew",pady=20)

        self.grid_container.grid_rowconfigure(1, weight=1)
        self.grid_container.grid_columnconfigure(0, weight=1)


        self.progressbar = ctk.CTkProgressBar(self.window, orientation="horizontal")
        
        self.manga_list = []
        
        # This is slow
        self.covers = []
        
        #self.update_image_cover(manga_title,None)
        #manga_id,fileName = get_manga_cover(manga_title)
        #image_cover = load_cover_image(manga_id,fileName,350,400)
        #self.image_cover = image_cover
        print(self.covers)

        #self.max_manga_num = 10
        # maximum sollte standard in der api 10 sein
        self.manga_num = len(self.result)



        loader = CTkLoader(master=window, opacity=0.8, width=40, height=40)
        window.after(500, loader.stop_loader) 

        # Für Linux 
        try:
            self.scrollable_frame.bind_all("<Button-4>",
            lambda e: self.scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
            self.scrollable_frame.bind_all("<Button-5>",
            lambda e: self.scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
        except Exception as e:
            print(e)


    def switch_manga_list(self,choice):
        if choice == "show popular manga":
            self.show_popular_manga()
        else:
            random_manga_list = self.get_random_manga()
            self.show_random_manga(random_manga_list)
    
    def get_random_manga(self) -> list:
        random_manga_list = get_random_manga()
        return random_manga_list

    def show_popular_manga(self):
        self.update_image_cover(self.popular_manga[0],None)
        self.display_mangas(self.popular_manga,len(self.popular_manga))
    def show_random_manga(self,random_manga):
        self.update_image_cover(random_manga[0],None)
        self.display_mangas(random_manga,len(random_manga))

    def update_image_cover(self,manga,manga_list=None) :

        manga_id, fileName = get_manga_cover(manga)
        self.image_cover = load_cover_image(manga_id, fileName, 350, 400)
        #self.covers.append(self.image_cover)
        

        #for manga in manga_list:
        #        manga_id,fileName = get_manga_cover(manga)
        #        self.manga_list.append((manga_id))
        #        self.manga_list.append((fileName))
        #        image_cover = load_cover_image(manga_id,fileName,350,400)
        #        self.covers.append(image_cover)
    
    def update_manga(self, new_title):
        self.manga_title = new_title
        self.result = search_manga_result(new_title)
        self.manga_num = len(self.result)
        
        self.update_image_cover(new_title,None)
        print(self.covers)
        
        self.display_mangas(self.result,len(self.result))



    def check_manga_exist(self,manga_name):
        path = f"Mangadex/{manga_name}"
        if os.path.exists(path):
            print("Manga exists",manga_name)
        else:
            d = CollectMangaInfos(manga_name,self.window)
            error = d.download_manga()
        
            return error

    def clear_all_ui_elements(self):
        #self.scrollable_frame.grid_forget()
            
            for widget_0 in self.window.winfo_children():
                widget_0.destroy()

            for widget in self.main_frames:
                widget.destroy()
            

            #self.search_field.destroy()
            #self.search_btn.destroy()
            #self.entry_frame.destroy()

    def message_box_func(self,error):
        if error:
            CTkMessagebox(
                self.window,

                title="Error",
                message=f"Failed  downloading ",
                icon="cancel",
                justify="center"
            )
        else:
            CTkMessagebox(self.window,
            title="Downloading ...",
            message=f"Dowloading Manga now. This might take a while",
            icon="info",
            justify="center")

    def open_manga(self,r):
        print("Downloading Manga now: ",manga_name)
        error = self.check_manga_exist(r)
        if not error :
            write_data_to_json("manga_data","manga_title",r)
            write_data_to_json("user_var",f"{r}",0)


            self.clear_all_ui_elements()
            ChapterView(r,self.window)
        else:
            self.message_box_func(True)

    def display_mangas(self,result,length,):
        

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()



        for i in range(length):

                row = i // 3
                col = i % 3

                block = ctk.CTkFrame(self.scrollable_frame,width=350,height=350,fg_color="transparent",corner_radius=0)
                block.grid(row=row,column=col ,padx=75,pady=50)

                text_block = ctk.CTkFrame(self.scrollable_frame,width=400,height=100,fg_color="transparent",corner_radius=0)
                text_block.grid(row=row,column=col,padx=28,pady=0,sticky="se")


                try:
                    block_label = ctk.CTkLabel(
                    text_block,text=f"{result[i]}",compound="left",font=(None,20,"bold"),text_color="white",
                    fg_color="transparent")
                except Exception as e:
                    print(e)



                block_label.place(x=5,y=0)
                
                try:
                    block_image = ctk.CTkLabel(block,text=f"",image=self.image_cover)
                    block_image.place(x=0,y=0)
                except Exception as e:
                    print("block image:",e)
                    self.covers = []
                # description label
                curr_manga = block_label.cget("text")


                open_btn = ctk.CTkButton(text_block,text="Open",fg_color=f"{button_color}",font=(None,20),
                hover_color=f"{button_hover_color}",command= lambda r=curr_manga: self.open_manga(r))
                open_btn.place(x=5,y=50)






