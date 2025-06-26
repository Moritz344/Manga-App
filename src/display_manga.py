import customtkinter as ctk
from handling_requests import *
from PIL import Image
import tkinter.font as tkFont
from json_utils.settings import *
from json_utils.write_to_json import write_data_to_json
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from tkinter import filedialog
import random
import shutil
from CTkToolTip import *
import threading
import functools
from get_downloaded_mangas import downloaded_mangas,get_pages_from_downloaded_mangas
from json_utils.delete_json_data import delete_data_in_json
from utils.ctkloader import CTkLoader

def start_main_screen_in_thread(window,manga_title):

    def check_thread():
        if t.is_alive():
            window.after(200,check_thread)
        else:
            loader.stop_loader()



    t = threading.Thread(target=lambda: main_window_frame(window,manga_title),daemon=True)
    t.start()

    loader = CTkLoader(master=window,)
    window.after(200,check_thread())


def main_window_frame(window,manga_title):


    def get_manga_with_name():
        window.focus()
        manga_title = search_field.get()
        c.update_manga(manga_title)

    def change_dots_icon_enter(event):
        points_settings.configure(image=black_dots_icon)
    def change_dots_icon_leave(event):
        points_settings.configure(image=dots_icon)

    def open_settings():
        s = Settings(window)

    def show_frame(frame):
        frame.tkraise()

    window.grid_columnconfigure(0,weight=1)
    window.grid_rowconfigure(0,weight=0)
    window.grid_rowconfigure(1,weight=1)


    main_container = ctk.CTkFrame(window,fg_color="transparent")
    main_container.grid(row=0,column=0,sticky="nsew",rowspan=2)

    main_container.grid_rowconfigure(0, weight=0)
    main_container.grid_rowconfigure(1, weight=3)

    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)


    settings_icon = ctk.CTkImage(Image.open("assets/icons/settings.png"),size=(50,50))
    history_icon = ctk.CTkImage(Image.open("assets/icons/history.png"),size=(50,50))
    github_icon = ctk.CTkImage(Image.open("assets/icons/github.png"),size=(50,50))
    search_image = ctk.CTkImage(Image.open("assets/icons/search.png"),size=(40,40))
    search_image_small = ctk.CTkImage(Image.open("assets/icons/search.png"),size=(20,20))
    dots_icon = ctk.CTkImage(Image.open("assets/icons/dots.png"),size=(20,20))
    black_dots_icon = ctk.CTkImage(Image.open("assets/icons/black_dots.png"),size=(20,20))


    settings_frame = ctk.CTkFrame(main_container,width=100,height=1080,fg_color="#1B1E20",corner_radius=0)
    settings_frame.grid(row=1,column=0,sticky="nsew")

    entry_frame = ctk.CTkFrame(main_container,height=200,width=1080,fg_color="#31363B",corner_radius=0)
    entry_frame.grid(row=0,column=0,padx=0,columnspan=2,sticky="nsew")

    main_frame = ctk.CTkFrame(main_container,width=2000,height=2000,fg_color="transparent")
    main_frame.grid(row=1,column=1,padx=0,sticky="nsew")

    small_search_bar = ctk.CTkEntry(settings_frame,placeholder_text="Search",height=50,width=290,font=(None,20),)
    small_search_bar.grid(row=0,column=0,padx=5,pady=20,sticky="nsew")

    small_search_btn = ctk.CTkButton(settings_frame,image=search_image,text="",width=10,height=0,font=(None,10),)
    small_search_btn.grid(row=0,column=1,padx=5,pady=0,)

    points_settings = ctk.CTkButton(entry_frame,text="",width=10,hover_color="#31363B",fg_color="#31363B",image=dots_icon)
    points_settings.pack(side="right",padx=5,pady=5,)

    settings_btn = ctk.CTkButton(settings_frame,text="Settings",image=settings_icon,font=(None,20),command=open_settings,
                                 compound="left",anchor="w",fg_color="#31363B")
    settings_btn.grid(row=1,column=0,padx=10,pady=20,sticky="nsew")

    history_btn = ctk.CTkButton(settings_frame,text="History",image=history_icon,font=(None,20),
                                anchor="w",fg_color="#31363B")
    history_btn.grid(row=2,column=0,padx=10,pady=20,sticky="nsew")


    search_field = ctk.CTkEntry(entry_frame,
    width=500,
    height=50,
    font=(None,20),
                            placeholder_text="Search Manga ...",
    placeholder_text_color="#B3B3B3",
    )


    search_btn = ctk.CTkButton(entry_frame,
    text="",
    width=20,
    height=50,
    font=(None,20),
    command=lambda :get_manga_with_name(),
    image=search_image)

    search_field.pack(anchor="e",padx=600,pady=10)
    search_btn.place(x=690,y=10)



    #show_frame(main_frame)




    popular_manga = get_popular_manga()


    c = DisplayMangaInfos(None,main_frame,main_container,popular_manga)
    c.update_manga(manga_title)
     #c.show_popular_manga()

    #c.show_popular_manga()


    points_settings.bind("<Enter>",change_dots_icon_enter)
    points_settings.bind("<Leave>",change_dots_icon_leave)


    return manga_title

class CollectMangaInfos(object):
    _instance_cache = {}
    def __new__(cls,manga_title,window,):
        
        key = (manga_title,)

        if key in cls._instance_cache:
            return cls._instance_cache[key]
        
        instance = super().__new__(cls)
        cls._instance_cache[key] = instance

        return instance

    def __init__(self,manga_title,window):
        self.window = window
        print()
        manga_id = get_manga_title(manga_title)
        print()
        
        self.chapters= get_manga_chapters(manga_id)
        #print(self.chapters)

        self.manga_id = manga_id
        self.manga_title = manga_title
        
        CTkMessagebox(
        self.window,
        title="Downloading",
        font=(None,15),
        icon="assets/icons/coffee.png",
        message = f"Grab a coffee while we download your manga using these settings: {chapter_download}")
 
    

    def start_download_thread(self):
        # startet download_manga in einem thread -> app freezed nicht
        threading.Thread(target=self.download_manga,daemon=True).start()

    def download_manga(self):
        error = ""
        try:
                for i,(chapter_id,chapter_number) in enumerate(self.chapters):
                    result = get_server_data(chapter_id)
                    if result is None:
                        return
                    pages,host,chapter_hash = result
                    
                    

                    downloading_chapters(pages,chapter_number,self.manga_title,host,chapter_hash)


                #print("id,num: ",chapter_id,chapter_number)
            #print("pages,host,hash",pages,host,chapter_hash)
                    
                
                                   
                
        except Exception as e:
            error = e
            return error
        

class ReadMangaScreen:
    _instance_cache = {}
    def __new__(cls,manga_title,window,chapter_start):
        
        key = (manga_title,)

        if key in cls._instance_cache:
            return cls._instance_cache[key]
        
        instance = super().__new__(cls)
        cls._instance_cache[key] = instance

        return instance

    def __init__(self,manga_title,window,chapter_start):

        self.manga_title = manga_title
        self.window = window

        self.main_container = ctk.CTkFrame(window)
        self.main_container.grid(row=0,column=0,sticky="nsew")

        window.grid_rowconfigure(0,weight=1)
        window.grid_columnconfigure(0,weight=1)


        self.manga_path = f"{manga_location}/{manga_title}"
        self.chapter_start = chapter_start

        self.chapter_number = 0
        #print("DEBUG",chapter_start)
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

        pages_len = get_pages_from_downloaded_mangas(self.manga_title,self.current_chapter_number)
        self.pages_len = pages_len


        self.chapter_list = os.listdir(self.manga_path)

        self.main_container.grid_columnconfigure(3,weight=1)
        self.main_container.grid_rowconfigure(0,weight=1)
        self.main_container.grid_rowconfigure(1,weight=4)

        self.option_field_2 = ctk.CTkFrame(self.main_container,fg_color="gray")
        self.option_field_2.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)


        self.option_field = ctk.CTkFrame(self.main_container,fg_color="gray")
        self.option_field.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        #self.manga_title_label = ctk.CTkLabel(self.option_field,text=f"{self.manga_title}",font=(None,30))
        #self.manga_title_label.pack(padx=0,pady=0)

        self.back_button = ctk.CTkButton(self.option_field,text="Back",font=(None,30),
        command= lambda: self.search_screen(),fg_color=f"{button_color}",hover_color=f"{button_hover_color}")
        self.back_button.pack(side="bottom",anchor="s",padx=0,pady=10)
        self.chapter_label = ctk.CTkLabel(self.option_field,text=f"Chapter: {self.chapter_number}",font=(None,30))
        self.chapter_label.pack()

        self.manga_field = ctk.CTkFrame(self.main_container,fg_color="gray")
        self.manga_field.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)


        chapter_var = tk.StringVar(value=f"Chapter_1")
        self.chapter_combobox = ctk.CTkComboBox(self.option_field,font=(None,15),width=150,height=50,
        values=self.chapter_list,variable=chapter_var)
        self.chapter_combobox.pack(anchor="w",padx=0,pady=10)

        page_var = tk.StringVar(value=f"Page_0")
        self.page_combobox = ctk.CTkComboBox(self.option_field,font=(None,15),width=150,height=50,
        values=self.pages_list,variable=page_var)
        self.page_combobox.pack(anchor="w",padx=0,pady=10)
        self.update_combobox(self.current_chapter_number)



        self.next_page_btn = ctk.CTkButton(self.option_field_2,text="",image=self.arrow_image_right,
        command=self.next_page,fg_color=f"{button_color}",hover_color=f"{button_hover_color}")
        self.next_page_btn.pack(side="right",padx=0,pady=0)
        #self.next_page_btn.place(x=0,y=0)

        self.prev_page_btn = ctk.CTkButton(self.option_field_2,text="",command=self.prev_page,
        fg_color=f"{button_color}",hover_color=f"{button_hover_color}",image=self.arrow_image_left)
        self.prev_page_btn.pack(side="left",padx=0,pady=0)

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

    def update_combobox(self,curr_chapter):
        pages_list = []
        new_pages = get_pages_from_downloaded_mangas(self.manga_title,curr_chapter)

        for page in range(new_pages):
            pages_list.append(str(f"Page_{page}"))

        self.page_combobox.configure(values=pages_list)

        del pages_list

    def next_chapter(self):
        #print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number <= self.chapter_number - 1:
                self.current_page_number = 0
                self.current_chapter_number += 1
                self.update_combobox(self.current_chapter_number)
                self.update_image(self.current_page_number,self.current_chapter_number)
                self.manga_image_label.configure(image=self.manga_page_image)
                self.update_pages_counter(self.current_chapter_number )
                write_data_to_json("user_var",f"{self.manga_title}",self.current_chapter_number)
    def prev_chapter(self):
            print(self.current_chapter_number,self.chapter_number)
            if self.current_chapter_number > 0:
                self.current_page_number = 0
                self.current_chapter_number -= 1
                self.update_combobox(self.current_chapter_number)
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
        #print(f"get_pages_chapters: {self.manga_path}/Chapter_{self.current_chapter_number}/Page_{self.current_page_number}")

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
        start_main_screen_in_thread(self.window,self.manga_title)

    def get_manga_information(self):
        manga_id = get_manga_title(self.manga_title)


        self.get_pages_chapters()

class ChapterView:
    
    _instance_cache = {}

    def __new__(cls,manga_title,window):

        key = (manga_title,)

        if key in cls._instance_cache:
            return cls._instance_cache[key]
        
        instance = super().__new__(cls)
        cls._instance_cache[key] = instance

        return instance

    def __init__(self,manga_title,window):

        self.window = window
        self.path = f"{manga_location}/{manga_title}"
        self.chapter_list = []
        self.curr_block = ""
        self.all_chapters = None
        self.description = None
        self.genres: list = None
        self.manga_status: str = None


        self.main_container = ctk.CTkFrame(window,fg_color="transparent")
        self.main_container.grid(row=0,column=0,)

        self.main_container.grid_columnconfigure(0,weight=1)
        self.main_container.grid_columnconfigure(1,weight=0)
        self.main_container.grid_rowconfigure(0,weight=1)




        self.frame_1 = ctk.CTkFrame(self.main_container,height=850,width=1000,fg_color="#242423",corner_radius=10)
        self.frame_1.grid(row=0,column=0,padx=(20,20),pady=10,)

        self.cover_frame = ctk.CTkFrame(self.frame_1,width=600,height=400,fg_color="transparent")
        self.cover_frame.place(x=10,y=10,)

        self.info_frame = ctk.CTkFrame(self.frame_1,width=600,fg_color="transparent")
        self.info_frame.place(x=300,y=10)



        self.frame_0 = ctk.CTkFrame(self.main_container,fg_color="transparent")
        self.frame_0.grid(row=0,column=1,padx=0,pady=10,sticky="n")

        self.manga_title: str = manga_title
        manga_id,filename = get_manga_cover(self.manga_title)

        image_cover = load_cover_image(manga_id,filename,250,300)
        
        self.cover_label = ctk.CTkLabel(self.cover_frame,text="",anchor="s",image=image_cover)
        self.cover_label.pack(side="left",padx=0,pady=0,anchor="ne")


        if len(self.manga_title) >= 36:
            short_manga_title = self.manga_title[:36] + "..."
        else:
            short_manga_title = self.manga_title

        self.get_all_chapters()
        self.title_label = ctk.CTkLabel(self.info_frame,text=f"{short_manga_title}",font=(None,30))
        self.title_label.pack(anchor="w",padx=0,pady=0,)
        


        self.chapter_text= ctk.CTkLabel(self.info_frame,text=f"all chapters",font=(None,20),
        text_color=f"{button_hover_color}")
        self.chapter_text.pack(anchor="w",padx=0,pady=0,)

        self.chapter_label= ctk.CTkLabel(self.info_frame,text=f"{self.all_chapters }",font=(None,30,"bold"))
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
            font=(None,30,),width=270,hover_color="#235730",command=lambda: self.start_over_func(0))

        self.start_over.place(x=10,y=400,)

        self.description_text = ctk.CTkLabel(self.frame_1,text=f"Description",
        text_color=f"{button_hover_color}",font=(None,25))
        self.description_text.place(x=10,y=490,)
        

        
        self.desc_frame = ctk.CTkScrollableFrame(self.frame_1,width=500,height=200,)
        self.desc_frame.place(x=10,y=530)
        
        self.description_label = ctk.CTkLabel(self.desc_frame,text=f"{self.description}",font=(None,20),
        justify="left",wraplength=500)
        self.description_label.pack(side="left",padx=0,pady=0)
        
        
        self.chapter_frame = ctk.CTkScrollableFrame(self.frame_0,width=750,height=750,fg_color="transparent")
        self.chapter_frame.pack(side="left",padx=10,pady=100,anchor="ne")




        self.combobox_var = ctk.StringVar(value="Start From First")
        self.order_chapter = ctk.CTkComboBox(self.frame_0,
        values=["Start From Last","Start From First"],state="readonly",variable=self.combobox_var,
                                             command=self.combobox_order)
        self.order_chapter.place(x=15,y=60)

        self.delete_btn = ctk.CTkButton(self.frame_1,text="Delete Manga",
        font=(None,20),fg_color="#e05033",hover_color=f"#a5250b",command=lambda: self.delete_manga(True))
        self.delete_btn.place(x=200,y=770)

       
        self.back_button = ctk.CTkButton(self.frame_1,text="Back",font=(None,20),fg_color=f"{button_color}",
                                             hover_color=f"{button_hover_color}",command=self.back_btn)
        self.back_button.place(x=10,y=770)


        

        self.manga_status_text_label = ctk.CTkLabel(self.info_frame,text="Manga Status",font=(None,20)
        ,text_color=f"{button_hover_color}")
        self.manga_status_text_label.pack(anchor="w",padx=0,pady=0)

        self.manga_status_label = ctk.CTkLabel(self.info_frame,text=f"{self.manga_status}",font=(None,20))
        self.manga_status_label.pack(anchor="w",padx=0,pady=0)

        try:
            self.chapter_frame.bind_all("<Button-4>",
            lambda e: self.chapter_frame._parent_canvas.yview("scroll", -1, "units"))
            self.chapter_frame.bind_all("<Button-5>",
            lambda e: self.chapter_frame._parent_canvas.yview("scroll", 1, "units"))
        except Exception as e:
            print(e)



    def start_chapter_view(self):
        self.manga_status_handler()
        self.get_description_len()
        self.get_chapters()
        self.combobox_order(self.combobox_var.get())

    def start_chapter_view_in_thread(self):

        def check_thread():
            if t.is_alive():
                self.main_container.after(200,check_thread)
            else:
                loader.stop_loader()


        loader = CTkLoader(master=self.main_container,)
        loader.update()

        t = threading.Thread(target=self.start_chapter_view,daemon=True)
        t.start()

        self.main_container.after(200,check_thread)

    def manga_status_handler(self):
        manga_id = get_manga_title(manga_title)
        manga_status = get_manga_status(manga_id)
        self.manga_status = manga_status


    def get_description_len(self):
        if hasattr(self,"_desc_len"):
           return self._desc_len

        text = self.description_label.cget("text") 
        self._desc_len = len(text)



    def delete_manga(self,show_message):
        try:
            if os.path.exists(self.path):
                delete_data_in_json(self.manga_title)
                shutil.rmtree(self.path)
                #print(f"Successfully Removed: {self.path}")
                if show_message:
                    CTkMessagebox(
                    self.window,
                    title="Remove Manga",
                    message=f"Successfully Removed {self.manga_title}",
                    icon="cancel",justify="center")
                self.back_btn()
        except Exception as e:
            print("in delete manga ",e)
    
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
                corner_radius=10,
                anchor="ne",
                font=(None,30,"bold"),fg_color=f"#242423",
                hover_color="#474444",
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
                corner_radius=10,
                anchor="ne",
                font=(None,30,"bold"),fg_color=f"#242423",hover_color=f"#474444",
                command= lambda m=self.curr_block: self.read_manga(m))

                block.pack(padx=0,pady=5,anchor="w")
                # get the current chapter the user wants to start at
                self.curr_block = i - 1
                print("curr_block",self.curr_block)


    def clear_all_ui_elements(self):
        try:
            for w in self.main_container.winfo_children():
                w.destroy()

        except Exception as e:
            print(e)
    def back_btn(self):
        self.clear_all_ui_elements()
        start_main_screen_in_thread(self.window,self.manga_title)

class DisplayMangaInfos:

    _instance_cache = {}
    def __new__(cls,manga_title,window,main_frames,popular_manga):
        
        key = (manga_title,tuple(popular_manga))

        if key in cls._instance_cache:
            return cls._instance_cache[key]
        
        instance = super().__new__(cls)
        cls._instance_cache[key] = instance

        return instance

    def __init__(self,manga_title,window,main_container,popular_manga):
        

        self.mangas_installed = None
        self.mangas_to_mark = None
        self.manga_title = manga_title
        self.window = window
        self.popular_manga = popular_manga
        self.main_container = main_container
        self._initialized = True
        self.manga_name_len = 20

        # ergebnis der mangas beim suchen
        self.result = search_manga_result(manga_title)

        self.download_icon = ctk.CTkImage(Image.open("assets/icons/download.png"),size=(30,30))

        self.grid_container = ctk.CTkFrame(self.window,width=1500,fg_color="transparent")
        self.grid_container.pack(padx=10,pady=10)

        self.checkbox_random_var = ctk.StringVar(value="off")
        self.checkbox_random = ctk.CTkCheckBox(self.grid_container,
        text="Random",
        variable=self.checkbox_random_var,
        onvalue="on",
        offvalue="off",
        corner_radius=50,
        font=(None,font_size),
        command = self.switch_to_random,
        hover_color=f"{button_hover_color}")
        self.checkbox_random.grid(sticky="w",row=0,column=0,pady=10,padx=80)

        self.checkbox_popular_var = ctk.StringVar(value="off")
        self.checkbox_popular = ctk.CTkCheckBox(self.grid_container,
        text="Popular",
        onvalue="on",
        offvalue="off",
        variable=self.checkbox_popular_var,
        corner_radius=50,
        font=(None,font_size),
        command = self.switch_to_popular,
        hover_color=f"{button_hover_color}")

        self.checkbox_popular.grid(sticky="w",row=0,column=0,pady=10,padx=240)

        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.grid_container, 
        width=1500,height=800,fg_color=f"{dark_charcoal}",
        scrollbar_button_color=f"{button_color}",scrollbar_button_hover_color=f"{button_hover_color}")
        self.scrollable_frame.grid(row=1,column=0,sticky="nsew",pady=0,padx=0)


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




        # Für Linux 
        try:
            self.scrollable_frame.bind_all("<Button-4>",
            lambda e: self.scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
            self.scrollable_frame.bind_all("<Button-5>",
            lambda e: self.scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
        except Exception as e:
            print(e)

        self.installed_mangas()




    def installed_mangas(self,):
        self.mangas_installed = downloaded_mangas()
        #print(mangas_installed)

    def check_list_for_installed(self,list_of_mangas):
        mark_this_manga = []
        for manga in list_of_mangas:
            for manga_2 in self.mangas_installed:
                if manga == manga_2:
                    #print(f"Manga: {manga} is installed.")
                    mark_this_manga.append(manga)

        return mark_this_manga

    def switch_to_random(self):
        if self.checkbox_random_var.get() == "on" :
            if self.checkbox_popular.get() == "off":
                random_manga_list = self.get_random_manga()
                self.show_random_manga(random_manga_list)
                self.checkbox_popular.configure(state=tk.DISABLED)
        else:
             self.checkbox_popular.configure(state=tk.NORMAL)

    def switch_to_popular(self):
        if self.checkbox_popular_var.get() == "on":
            if self.checkbox_random.get() == "off":
                self.show_popular_manga()
                self.checkbox_random.configure(state=tk.DISABLED)
        else:
             self.checkbox_random.configure(state=tk.NORMAL)
    
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
        self.image_cover = load_cover_image(manga_id, fileName, 300, 300)
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
        path = f"{manga_location}/{manga_name}"
        if os.path.exists(path):
            print("Manga exists",manga_name)
        else:
            d = CollectMangaInfos(manga_name,self.window,)
            err = d.start_download_thread()
        
            return err

    def clear_all_ui_elements(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()


    def open_manga(self,r,curr):
        print("Downloading Manga now: ",manga_name)
        err = self.check_manga_exist(r)
        if not err:
            write_data_to_json("manga_data","manga_title",r)
            write_data_to_json("user_var",f"{r}",0)


            self.clear_all_ui_elements()

            #ReadMangaScreen(r,self.main_container,1)
            c = ChapterView(r,self.main_container)
            c.start_chapter_view_in_thread()



    def display_mangas(self,result,length,):
        

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


        for i in range(length):

                row = i // 3
                col = i % 3

                block = ctk.CTkFrame(self.scrollable_frame,
                width=350,height=350,fg_color="transparent",corner_radius=0)
                block.grid(row=row,column=col ,padx=75,pady=50)

                text_block = ctk.CTkFrame(self.scrollable_frame,width=400,height=100,
                fg_color="transparent",corner_radius=0)
                text_block.grid(row=row,column=col,padx=28,pady=0,sticky="se")



                try:
                    block_label = ctk.CTkLabel(
                    text_block,text=f"{result[i]}",compound="left",font=(None,font_size,"bold"),text_color="white",
                    fg_color="transparent")
                except Exception as e:
                    print(e)

                marked_box = ctk.CTkButton(text_block,
                text="",image=self.download_icon,fg_color="green",hover_color="#235730",width=50,
                font=(None,font_size,))




                block_label.place(x=5,y=0)

                try:
                    block_image = ctk.CTkLabel(block,text=f"",image=self.image_cover)
                    block_image.place(x=0,y=0)
                except Exception as e:
                    print("block image:",e)
                    self.covers = []
                # description label
                curr_manga = block_label.cget("text")
                full_manga_name = block_label.cget("text")
                # mark downloaded mangas as 'installed'
                mark = self.check_list_for_installed(result)
                if curr_manga in mark:
                    tooltip = CTkToolTip(marked_box,message="You have installed this manga.")
                    marked_box.place(x=250,y=50)


                # manga with long names get shortended
                if len(curr_manga) >= 30:
                    curr_manga = curr_manga[:30] + "..."

                block_label.configure(text=f"{curr_manga}")

                open_btn = ctk.CTkButton(text_block,text="Open",fg_color=f"{button_color}",font=(None,20),
                hover_color=f"{button_hover_color}",command= lambda r=full_manga_name: self.open_manga(r,curr_manga))
                open_btn.place(x=5,y=50)





class Settings:
    def __init__(self,window):
        # TODO: app theme / eigenes theme erstellen
        # TODO: Heruntergeladene Mangas löschen

        self.changed_setting = False

        self.window = window
        self.clear_ui_elements()

        self.display_icon = ctk.CTkImage(Image.open("assets/icons/display_100.png"),size=(25,25))
        self.general_icon = ctk.CTkImage(Image.open("assets/icons/settings.png"),size=(25,25))

        self.home_btn = ctk.CTkButton(
        self.window,
        text="Home",
        fg_color=f"{button_color}",
        hover_color=f"{button_hover_color}",
        command=self.home_screen,
        font=(None,20))

        self.side_frame = ctk.CTkFrame(self.window,height=900,)
        self.side_frame.grid(row=0,column=0,sticky="nsew",padx=(20,10),pady=20)
        

        self.main_frame = ctk.CTkFrame(self.window,width=1500,height=900,)
        self.main_frame.grid(row=0,column=1,sticky="nsew",padx=(20,10),pady=20)
        
        self.settings_btn_1 = ctk.CTkButton(self.side_frame,
        text="General",
        font=(None,20),
        image=self.general_icon,
        command=self.general_settings_tab,
        fg_color=f"{button_hover_color}",
        hover_color=f"{button_color}"

        )
        self.settings_btn_2 = ctk.CTkButton(self.side_frame,
        text="Display",
        image=self.display_icon,
        font=(None,20),
        compound="left",
        fg_color="transparent",
        hover_color=f"{button_hover_color}",
        command=self.display_tab

        )

        self.settings_btn_1.pack(anchor="center",padx=0,pady=20)
        self.settings_btn_2.pack(anchor="center",padx=0,pady=20)
        
        self.setting_frame_1 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500)
        self.setting_frame_2 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500)
        self.setting_frame_3 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500)
        self.setting_frame_4 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500)

        f_1 = ctk.CTkLabel(self.setting_frame_1,text="Font Size",font=(None,30),width=100)
        f_2 = ctk.CTkLabel(self.setting_frame_1,text="Change the ui font size.",width=100,font=(None,15))

        self.font_var = tk.IntVar(value=font_size)
        font_slider = ctk.CTkSlider(self.setting_frame_1,from_=0,to=30,
        variable=self.font_var,
        command=self.slider_event,)

        self.font_number_label = ctk.CTkLabel(self.setting_frame_1,
        text=f"{self.font_var.get()}",
        font=(None,20))

        self.font_number_label.place(x=14,y=90)
        font_slider.place(x=10,y=130)

        f_1.place(x=10,y=10)
        f_2.place(x=10,y=60)

        f_3 = ctk.CTkLabel(self.setting_frame_2,text="Chapter Download",font=(None,30),width=100)
        f_4 = ctk.CTkLabel(self.setting_frame_2,text="Change the amount of chapters to download",
        width=100,font=(None,15),
        )
        
        self.chapter_var = ctk.StringVar(value="Download All")
        self.values: list = ["Download All","Download Half","Download 10","Download 20","Download 30"]
        self.chapter_choices = ctk.CTkComboBox(self.setting_frame_2,values=self.values,
        state="readonly",command=self.chapter_amount,
        font=(None,15),width=150)
        self.chapter_choices.set(chapter_download)
        
        self.chapter_choices.place(x=10,y=100)

        f_3.place(x=10,y=10)
        f_4.place(x=10,y=60)

        f_5 = ctk.CTkLabel(self.setting_frame_3,text="Reset History",font=(None,30),width=100)
        f_6 = ctk.CTkLabel(self.setting_frame_3,text="Reset your current history ",width=100,font=(None,15))

        self.reset_btn = ctk.CTkButton(self.setting_frame_3,text="Reset",font=(None,20),
        fg_color="red",hover_color="#a05a58")
        self.reset_btn.place(x=10,y=100)

        f_5.place(x=10,y=10)
        f_6.place(x=10,y=60)

        f_7 = ctk.CTkLabel(self.setting_frame_4,text="Save Mangas",font=(None,30),width=100)
        f_8 = ctk.CTkLabel(self.setting_frame_4,text="Change the location for saving mangas",width=100,font=(None,15))
        
        self.manga_path_entry = ctk.CTkEntry(self.setting_frame_4,font=(None,20),width=600,
        placeholder_text="/home/bob/Mangas")
        self.manga_path_entry.insert(tk.END,f"{manga_location}")
        self.manga_path_entry.place(x=10,y=100)

        self.manga_path_btn = ctk.CTkButton(self.setting_frame_4,
        text="Open",font=(None,20),fg_color=f"{button_color}",hover_color=f"{button_hover_color}",
        command=self.open_file_manager)
        self.manga_path_btn.place(x=10,y=150)

        self.manga_path_save_btn = ctk.CTkButton(self.setting_frame_4,
        text="Save",font=(None,20),fg_color=f"{color_green}",hover_color=f"{button_hover_color}",
        command=self.save_manga_location)
        self.manga_path_save_btn.place(x=180,y=150)


        f_7.place(x=10,y=10)
        f_8.place(x=10,y=60)

        self.setting_frame_1.pack()
        self.setting_frame_2.pack()
        self.setting_frame_3.pack()
        self.setting_frame_4.pack()



        self.home_btn.grid(row=1,column=0,padx=30,pady=0,sticky="w")

        #self.insert_json()

    def chapter_amount(self,value):
        write_data_to_json("settings","chapter_download",value)

    def check_manga_path(self,path) -> str:
        # user has to give the full path if not the path is incorrect
        if os.path.exists(path):
            self.changed_setting = True
            print("Path exists: ",path)
            CTkMessagebox(self.window,justify="center",
            message=f"New manga path for mangas is saved in: {path}",
            icon="check",title="Changed Manga Path",option_1="OK")
            return path
        else:
            CTkMessagebox(self.window,justify="center",
            message="Path does not Exist. Please be sure to name the full path",
            icon="cancel",title="FileNotFoundError")
            print(f"Path {path} does not exist")
            path = manga_location
            self.manga_path_entry.delete(0,tk.END)
            self.manga_path_entry.insert(tk.END,path)
            return path
    
    def open_file_manager(self):
        try:
            file_path = filedialog.askdirectory(title="Open File",)
            path = self.check_manga_path(file_path)
            write_data_to_json("settings","manga_location",path)
            self.manga_path_entry.delete(0,tk.END)
            self.manga_path_entry.insert(tk.END,path)
        except Exception as e:
            print("open file manager:",e)


    def save_manga_location(self):
        self.changed_setting = True
        path = self.check_manga_path(self.manga_path_entry.get())
        write_data_to_json("settings","manga_location",path)
        print("Saved manga location:",path)

    def slider_event(self,value):
        self.font_number_label.configure(text=f"{self.font_var.get()}")
        write_data_to_json("settings","font_size",self.font_var.get())
                  
    def reset_grid_config(self) -> None:
        def reset_grid_config(self):
            self.window.grid_columnconfigure(0, weight=0)  # Seitenleiste
            self.window.grid_columnconfigure(1, weight=1)  # Hauptbereich
            self.window.grid_rowconfigure(0, weight=1)     # Zeile für Frames

    def clear_ui_elements(self) -> None:
        for widget in self.window.winfo_children():
            widget.destroy()

    def clear_settings_tab(self):
        self.settings_frames = [self.setting_frame_1,self.setting_frame_2,self.setting_frame_3,self.setting_frame_4]
        for i,v in  enumerate(self.settings_frames):
            for widget in self.settings_frames[i].winfo_children():
                widget.destroy()

    def general_settings_tab(self):
        self.clear_ui_elements()
        a = Settings(self.window)
        

    def home_screen(self) -> None:
        self.reset_grid_config()
        self.clear_ui_elements()
        start_main_screen_in_thread(self.window,manga_name)
        if self.changed_setting:
            CTkMessagebox(self.window,justify="center",
            message="Restart the app to see the changed settings in action!",icon="info",title="Settings")

    def save_theme_settings(self) -> None:
        self.changed_setting = True
        max_entry_length: int = 6   

        self.window.focus()


        background_color = self.background_entry.get()
        new_button_color = self.button_entry.get()
        new_text_color = self.text_color_entry.get() 

        #print("Background",background_color,len(background_color) - 1)
        #print("Button-COlor",button_color,len(button_color) - 1)
        #print("Text-Color",text_color,len(text_color) - 1)

        if len(background_color) - 1 <= max_entry_length:
            print("baclground color saved")
            write_data_to_json("settings","background",background_color)
        else:
            self.update_entry_box()
            CTkMessagebox(self.main_frame,justify="center",icon="cancel",title="Invalid Hex code",
            message="Invalid color.")
        if len(button_color) - 1 <= max_entry_length:
            print("button color saved")
            write_data_to_json("settings","button_color",new_button_color)
        else:
            self.update_entry_box()
            CTkMessagebox(self.main_frame,justify="center",icon="cancel",title="Invalid Hex code",
            message="Invalid color.")
        if len(text_color) - 1 <= max_entry_length:
            write_data_to_json("settings","text_color",new_text_color)
        else:
            self.update_entry_box()
            CTkMessagebox(self.main_frame,justify="center",icon="cancel",title="Invalid Hex code",
            message="Invalid color.")
            
    
    def update_entry_box(self):
        self.background_entry.delete(0,tk.END)
        self.text_color_entry.delete(0,tk.END)
        self.button_entry.delete(0,tk.END)

        self.background_entry.insert(0,f"{background}")
        self.text_color_entry.insert(0,f"{text_color}")
        self.button_entry.insert(0,f"{button_color}")

    def reset_colors_to_default(self):
        self.window.focus()
        self.background_entry.delete(0,tk.END)
        self.text_color_entry.delete(0,tk.END)
        self.button_entry.delete(0,tk.END)

        self.background_entry.insert(0,"#121212")
        self.text_color_entry.insert(0,"#f9f9f9")
        self.button_entry.insert(0,"#44414B")

    def change_colorscheme(self,choice):
        print(choice)
        write_data_to_json("settings","colorscheme",choice)
        

    def display_tab(self) -> None:
        self.clear_settings_tab()

        self.settings_btn_1.configure(fg_color=f"transparent")
        self.settings_btn_2.configure(fg_color=f"{button_hover_color}")

        self.display_frame_1 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500)
        self.display_frame_2 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500,)
        self.display_frame_3 = ctk.CTkFrame(self.main_frame,fg_color="transparent",width=1500,)
        
        ctk.CTkLabel(self.display_frame_2,text="Background-Color",font=(None,30)).place(x=10,y=10)
        self.background_entry = ctk.CTkEntry(self.display_frame_2,placeholder_text="#121212",
        font=(None,20),)
        self.background_entry.place(x=10,y=60)

        ctk.CTkLabel(self.display_frame_2,text="Button-Color",font=(None,30)).place(x=10,y=100)
        self.button_entry = ctk.CTkEntry(self.display_frame_2,placeholder_text="#44414B",
        font=(None,20),)
        self.button_entry.place(x=10,y=150)



        ctk.CTkLabel(self.display_frame_1,text="Theme",font=(None,30)).place(x=10,y=0)
        ctk.CTkLabel(self.display_frame_1,text="Customize your Theme",font=(None,20)).place(x=10,y=40)

        
        
        ctk.CTkLabel(self.display_frame_3,text="Colorscheme",font=(None,30)).place(x=10,y=100)
        self.colorscheme_var = ctk.StringVar(value=f"{colorscheme}") 
        self.colorscheme_box = ctk.CTkComboBox(self.display_frame_3,
        values=["Default","Dracula","Catppuccin"],variable=self.colorscheme_var,
        command=self.change_colorscheme)
        self.colorscheme_box.place(x=10,y=150)

        ctk.CTkLabel(self.display_frame_3,text="Text-Color",font=(None,30)).place(x=10,y=10)
        self.text_color_entry = ctk.CTkEntry(self.display_frame_3,placeholder_text="#f2f2f2",
        font=(None,20),)
        self.text_color_entry.place(x=10,y=60)

        self.save_btn = ctk.CTkButton(self.main_frame,text="Save",
        fg_color="green",hover_color="#235730",font=(None,20),
        command=self.save_theme_settings)

        self.reset_btn = ctk.CTkButton(self.main_frame,text="Reset",fg_color="red",font=(None,20),
        hover_color="#a05a58",command=self.reset_colors_to_default)

        self.reset_btn.place(x=200,y=730)
        self.save_btn.place(x=50,y=730)

        CTkToolTip(self.reset_btn,message="Reset colors to default colors")
        
        
        self.display_frame_1.place(x=50,y=50)
        self.display_frame_2.place(x=50,y=150)
        self.display_frame_3.place(x=50,y=400)

        self.update_entry_box()


