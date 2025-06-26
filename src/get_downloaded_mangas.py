import os
from json_utils.settings import mangas_downloaded,manga_location
import functools

@functools.lru_cache
def downloaded_mangas() -> list:
    installed_mangas = []

    for key,value in enumerate(mangas_downloaded):
        #print(key,value)
        installed_mangas.append(value)

    return installed_mangas


@functools.lru_cache
def get_pages_from_downloaded_mangas(manga_title,chapter_number) -> int:
    # return the length of pages the given chapter has

    path = f"{manga_location}/{manga_title}"
    chapter_list = os.listdir(f"{path}/Chapter_{chapter_number}")
    chapter_count = len(chapter_list)

    pages_len = 0

    x = os.listdir(f"{path}/Chapter_{chapter_number}")
    pages_len = len(x)


    return pages_len


