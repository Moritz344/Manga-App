from handling_requests import *
import threading
from CTkMessagebox import CTkMessagebox

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




    def start_download_thread(self):
        # startet download_manga in einem thread -> app freezed nicht
        threading.Thread(target=self.download_manga,daemon=True).start()
        CTkMessagebox(
        self.window,
        title="Downloading",
        font=(None,15),
        icon="assets/icons/coffee.png",
        message = f"Grab a coffee while we download your manga using these settings: {chapter_download}")

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
