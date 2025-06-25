import customtkinter as ctk
from utils.ctkgif import CTkGif

class CTkLoader(ctk.CTkFrame):
    def __init__(self, master: any, opacity: float = 0.8, width: int = 40, height: int = 40):
        self.master = master
        self.master.update()
        self.master_width = self.master.winfo_width()
        self.master_height = self.master.winfo_height()
        super().__init__(master, width=self.master_width, height=self.master_height, corner_radius=0)


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loader = CTkGif(self, "assets/icons/loader.gif", width=width, height=height)

        
        self.loader.grid(row=0, column=0, sticky="nsew")
        self.loader.start()

        self.place(relwidth=1.0, relheight=1.0)

    def stop_loader(self):
        self.loader.stop()
        self.destroy()

