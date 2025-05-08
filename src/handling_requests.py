import requests
import os

# doku: https://api.mangadex.org/docs/04-chapter/feed/

# -- Manga Search Engine

base_url = "https://api.mangadex.org"


manga_title = input("Manga title: ")
manga_title_response = requests.get(f"{base_url}/manga?title={manga_title}")

def get_manga_title(manga_title,manga_title_response):
    if manga_title_response.status_code == 200:
            manga_data = manga_title_response.json().get("data")
    
            manga_id = manga_data[0]["id"]
            print("Manga id",manga_id)
    else:
        manga_id = None

    return manga_id
manga_id = get_manga_title(manga_title,manga_title_response)

feed_url = f"{base_url}/manga/{manga_id}/feed?translatedLanguage[]=en&order[chapter]=asc"
feed_response = requests.get(feed_url)
def get_manga_chapters(feed_response,):
    if feed_response.status_code == 200:
        chapters = feed_response.json()["data"]
        
        
        # get all chapters
        for i,chapter in enumerate(chapters):
                chapter_manga = chapters[i]
                chapter_id = chapter_manga["id"]
                chapter_number = chapter_manga["attributes"].get("chapter")
        
        # get one chapter for testing
        first_chapter = chapters[0]
        chapter_1_id = first_chapter["id"] 
        chapter_1_num = first_chapter["attributes"].get("chapter") 


    return chapter_id,chapter_number,chapter_1_id,chapter_1_num
chapter_id,chapter_number,chapter_1_id,chapter_1_num = get_manga_chapters(feed_response)

def get_server_data():
    server_response = requests.get(f"{base_url}/at-home/server/{chapter_id}")
    if server_response.status_code == 200:
        server_data = server_response.json()
        
        host = server_data["baseUrl"]
        chapter_hash = server_data["chapter"]["hash"]
        pages = server_data["chapter"]["data"]
    
    return pages,host,chapter_hash
pages,host,chapter_hash = get_server_data()


def downloading_chapters(pages,chapter_1_num):
    chapter_1_num = int(chapter_1_num)
    for num in range(chapter_1_num):
        num += 1
        folder_path = f"Mangadex/{manga_title}/Chapter_{num}"
        os.makedirs(folder_path,exist_ok=True)
    
        for page in pages:
            image_url = f"{host}/data/{chapter_hash}/{page}"
            image_response = requests.get(image_url)
            with open(f"{folder_path}/{page}","wb") as file:
                file.write(image_response.content)
        print(f"Downloaded {len(pages)} pages.")
    else:
        print("Path already exists.")
    
    

downloading_chapters(pages,chapter_1_num)





