import requests
from main import *
import rich
from termcolor import colored,cprint

base_url = "https://api.mangadex.org"

# global vars
def input_handler():
    user_input = input("Manga title:(if you know) ")
    include_tags = input("Included Genres: ")
    exclude_tags = input("Excluded Genres: ")
    status = input("Manga Status: ")
    manga_limit = input("Maximum of Mangas to show: ")

    if not manga_limit:
        manga_limit = 20
    if not status:
        status = "ongoing,completed"
    
    return user_input,include_tags,exclude_tags,manga_limit,status
user_input,include_tags,exclude_tags,manga_limit,status = input_handler()



manga_status = status.split(",")
included_tag_names = include_tags.split(",")
excluded_tag_names = exclude_tags.split(",")

print("DEBUG:",included_tag_names,excluded_tag_names)





# -- Wir wandeln die tags in uuids um
tags = requests.get(f"{base_url}/manga/tag").json()
included_tag_ids = [
    tag["id"]
    for tag in tags["data"]
    if tag["attributes"]["name"]["en"]
       in included_tag_names
]

excluded_tag_ids = [
    tag["id"]
    for tag in tags["data"]
    if tag["attributes"]["name"]["en"]
        in excluded_tag_names
]
# --



manga_title = user_input

response = requests.get(f"{base_url}/manga?title={manga_title}")
response_2 = requests.get(f"{base_url}/manga",
    params={
        "includedTags[]": included_tag_ids,
        "excludedTags[]": excluded_tag_ids,
        "limit":manga_limit,
        "title":user_input,
        "status[]":manga_status,
    },
)



def manga_information(data):
    manga_id = data["data"][0]["id"]
    #print(manga_id)

def format_output(titles):
        print()
        print("Excluded Tags: ",excluded_tag_names,"Included Tags: ",included_tag_names)
        print("Manga Status: ",manga_status)
        print()
        print("Manga search result.")
    
        for i,v in enumerate(titles):
            print(i,v)
        print()

def response_handler():
    if response.status_code == 200:
        #data = response.json()
        #manga_information(data)
        #print(data)
        pass
    else:
        print(response.status_code)
    if response_2.status_code == 200:
        titles = [
            manga["attributes"]["title"].get("en")
            for manga in response_2.json().get("data", [])
        ]
        status_list = [
            manga["attributes"].get("status")
            for manga in response_2.json().get("data", [])
        ]
        
        format_output(titles)

    else:
        print(response_2.status_code)

response_handler()
