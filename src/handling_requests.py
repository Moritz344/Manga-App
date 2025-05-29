import requests
import os
import shutil
from PIL import Image,ImageTk
import io
# doku: https://api.mangadex.org/docs/04-chapter/feed/

# -- Manga Search Engine

base_url = "https://api.mangadex.org"
manga_title = None

def search_manga_result(manga_title="Frieren"):
    r = requests.get(f"{base_url}/manga?title={manga_title}")
    manga_data = r.json()

    results = []

    if r.status_code == 200:
        for index in manga_data["data"]:
            try:
                #name = manga_data["data"][index]["attributes"]["title"]["en"]
                name = index["attributes"]["title"]["en"]
                results.append(name)
            except Exception as e:
                print("DEBUG:",e)
            print(name)

    return results

def get_manga_cover(title):
    manga_id = get_manga_title(title)
    print(manga_id)
    print(f"getting cover for {title} with {manga_id}")

    cover_url = f"https://api.mangadex.org/cover?manga[]={manga_id}"
    
    r_1 = requests.get(cover_url)

    if r_1.status_code == 200:
        data = r_1.json().get("data")
        filename = data[0]["attributes"]["fileName"]


        #print(filename)
        print(r_1.status_code)

        return manga_id,filename
    else:
        print(r_1.status_code)


def load_cover_image(manga_id,filename):
        cover_image = f"https://uploads.mangadex.org/covers/{manga_id}/{filename}" 
        r = requests.get(cover_image)

        if r.status_code == 200:
            image_data = r.content
            image_cover = Image.open(io.BytesIO(image_data))
            image_cover = image_cover.resize((450,400))
            return ImageTk.PhotoImage(image_cover)
        else:
            print("Fehler beim laden des bildes:",r.status_code)


def get_manga_title(manga_title):
    try:
        manga_title_response = requests.get(f"{base_url}/manga?title={manga_title}")
        if manga_title_response.status_code == 200:
                manga_data = manga_title_response.json().get("data")

                manga_id = manga_data[0]["id"]
                #print("Manga id",manga_id)
        else:
            manga_id = None
    except Exception as e:
        print("DEBUG: ",e)
        print("Does this manga exist?")
    return manga_id

def get_manga_chapters(manga_id,):
        feed_url = f"{base_url}/manga/{manga_id}/feed?translatedLanguage[]=en&order[chapter]=asc"
        feed_response = requests.get(feed_url)

        if feed_response.status_code == 200:
            chapters = feed_response.json()["data"]

            if not chapters:
                print("no chapters found for this manga:",manga_id)

            chapter_list = []
            #print(chapter_list)

            # get all chapters
            for chapter in chapters:
                    #print(chapter)

                    chapter_id = chapter["id"]
                    chapter_number = chapter["attributes"].get("chapter")

                    if chapter_number == None:
                        return

                    chapter_list.append((chapter_id,chapter_number))
                    print("chapter number",chapter_number)

            ## get one chapter for testing
            #first_chapter = chapters[0]
            #chapter_1_id = first_chapter["id"]
            #chapter_1_num = first_chapter["attributes"].get("chapter")
            #print("num_1",chapter_1_num)
            ##print()
            ##print("Chapter id:",chapter_1_id,"Chapter num",chapter_1_num)


            return chapter_list


def get_server_data(chapter_id):
    server_response = requests.get(f"{base_url}/at-home/server/{chapter_id}")
    if server_response.status_code == 200:
        server_data = server_response.json()

        host = server_data["baseUrl"]
        chapter_hash = server_data["chapter"]["hash"]
        pages = server_data["chapter"]["data"]
        return pages,host,chapter_hash
    else:
        print("something went wrong in get_server_data",server_response.status_code)



def downloading_chapters(pages,chapter_number,manga_title,host,chapter_hash):
        chapter_number = int(chapter_number)
        print(chapter_number)
        for num in range(chapter_number):
            print("Started Downloading ...")
            folder_path = f"Mangadex/{manga_title}/Chapter_{num}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path,)

                for i,page in enumerate(pages):
                    image_url = f"{host}/data/{chapter_hash}/{page}"
                    image_response = requests.get(image_url)
                    with open(f"{folder_path}/Page_{i}","wb") as file:
                        file.write(image_response.content)
                print(f"Downloaded {len(pages)} pages.")
