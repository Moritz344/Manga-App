from json_utils.settings import manga_name
import random

settings_dic = {
    "s1": "Reading Manga ...",
    "s2": "Otaku Session 404",
    "s3": f"Last read {manga_name}",
    "s4": "It should have been me!",
    "s5": "Thats the end?",
    "s6": "Made with the Mangadex API"
}


def choose_session_name():
    global settings_dic
    session_list = []
    for key,value in settings_dic.items():
        #print(value)
        session_list.append(value)

    window_title = random.choice(session_list)

    return window_title

