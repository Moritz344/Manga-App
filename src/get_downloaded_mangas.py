#!/usr/bin/env python3

from settings import mangas_downloaded

def downloaded_mangas() -> list:
    installed_mangas = []

    for key,value in enumerate(mangas_downloaded):
        #print(key,value)
        installed_mangas.append(value)

    return installed_mangas


downloaded_mangas()
