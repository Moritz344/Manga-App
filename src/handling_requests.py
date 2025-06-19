import requests
import os
import shutil
from PIL import Image,ImageTk
import io
from concurrent.futures import ThreadPoolExecutor
from settings import manga_location,chapter_download
from nerd_debug import NerdCLI

# doku: https://api.mangadex.org/docs/04-chapter/feed/

# -- Manga Search Engine

base_url = "https://api.mangadex.org"
manga_title = None
nerd = NerdCLI()


def search_manga_result(manga_title) -> list:
    global nerd
    r = requests.get(f"{base_url}/manga?title={manga_title}")
    manga_data = r.json()

    results = []

    if r.status_code == 200:
        for index in manga_data["data"]:
            try:
                #name = manga_data["data"][index]["attributes"]["title"]["en"]
                name = index["attributes"]["title"]["en"]
                results.append(name)
                nerd.start_output(name)
            except Exception as e:
                print("Error in search_manga_result function: ",e)
            
    return results

def get_manga_status(manga_id) -> str:
    global nerd
    global base_url
    url = f"{base_url}/manga/{manga_id}"
    
    try:
        r = requests.get(url);
        if r.status_code == 200:
            data = r.json().get("data")

            manga_status = data["attributes"]["status"]
            nerd.print_status_code(r.status_code)
            
        else:
            nerd.print_status_code(r.status_code)
    except Exception as e:
        manga_status = "No Status Found"
        print("Error in (get_manga_status):",e)
    
    return manga_status

def get_random_manga() -> list:
    global base_url
    url = f"{base_url}/manga/random"
    random_manga_list = []

    try:
        for response in range(7):
            r = requests.get(url)

            if r.status_code == 200:
                data = r.json().get("data")

                random_manga = data["attributes"]["title"]["en"]
                random_manga_list.append(random_manga)

                nerd.start_output(random_manga)

                nerd.print_status_code(r.status_code)

            else:
                nerd.print_status_code(r.status_code)

    except Exception as e:
        random_manga_list = []
        print("DEBUG (random_manga)",e)
    return random_manga_list

def get_manga_genre(manga_id) -> list:
    global base_url
    url = f"{base_url}/manga/{manga_id}"

    response = requests.get(url)
    genre_list = []

    try:

        if response.status_code == 200:
            data = response.json().get("data")
            for i in range(len(data) - 1):
                genre = data["attributes"]["tags"][i]["attributes"]["name"]["en"]
                #print("GENRE",genre)
                genre_list.append(genre)


        else:
            nerd.print_status_code(r.status_code)

    except Exception as e:
        genre_list = ["No Genres found."]
        print("DEBUG:",e)

    return genre_list

def get_popular_manga() -> list:
    url = "https://api.mangadex.org/manga?limit=10&order[followedCount]=desc"

    r = requests.get(url)
    popular_manga = []

    if r.status_code == 200:
        data = r.json().get("data")
        
        for num in range(0,len(data)):
            try:
                title = data[num]["attributes"]["title"]["en"]
            except KeyError:
                title = data[num]["attributes"]["title"]["ja-ro"]
            popular_manga.append(title)

        return popular_manga

    else:
        print(r.status_code)

def get_manga_description(manga_id) -> str:
    global base_url
    url = f"{base_url}/manga/{manga_id}"

    response = requests.get(url)
    
    try:
        if response.status_code == 200:
            data = response.json().get("data")

            description = data["attributes"]["description"]["en"]

        else:
            print(nerd.print_status_code)


    except KeyError as e:
        description = "Description not found."
        print("DEBUG: (KeyError)",e)

    return description

def get_manga_cover(title):
    manga_id = get_manga_title(title)
    #print(manga_id)
    #print(f"getting cover for {title} with {manga_id}")

    cover_url = f"https://api.mangadex.org/cover?manga[]={manga_id}"
    
    r_1 = requests.get(cover_url)

    if r_1.status_code == 200:
        data = r_1.json().get("data")
        filename = data[0]["attributes"]["fileName"]


        #print(filename)
        print(nerd.print_status_code)

        return manga_id,filename
    else:
        print(nerd.print_status_code)


def load_cover_image(manga_id,filename,sizex,sizey):
        cover_image = f"https://uploads.mangadex.org/covers/{manga_id}/{filename}" 
        r = requests.get(cover_image)

        if r.status_code == 200:
            image_data = r.content
            image_cover = Image.open(io.BytesIO(image_data))
            image_cover = image_cover.resize((sizex,sizey))
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

def get_only_chapters(manga_id):
        feed_url = f"{base_url}/manga/{manga_id}/feed?translatedLanguage[]=en&order[chapter]=asc"
        feed_response = requests.get(feed_url)
        

        if feed_response.status_code == 200:
            chapters = feed_response.json()["data"]

            if not chapters:
                print("no chapters found for this manga:",manga_id)
                error = "404"

            # get all chapters
            for chapter in chapters:
                    chapter_number = chapter["attributes"].get("chapter")

            return chapter_number

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
                    #print("chapter number",chapter_number)

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
        path = manga_location

        chapter_to_download = None
        if chapter_download == "Download Half":
            chapter_to_download = chapter_number // 2
        elif chapter_download == "Download 10" and chapter_number >= 10:
            chapter_to_download = 10
        elif chapter_download == "Download 20" and chapter_number >= 10:
            chapter_to_download = 20
        elif chapter_download == "Download 30" and chapter_number >= 10:
            chapter_to_download = 30
        else:
            chapter_to_download = chapter_number
        
        

        for num in range(chapter_to_download):
            folder_path = f"{path}/{manga_title}/Chapter_{num}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path,)

                for i,page in enumerate(pages):
                    image_url = f"{host}/data/{chapter_hash}/{page}"
                    image_response = requests.get(image_url)
                    with open(f"{folder_path}/Page_{i}","wb") as file:
                        file.write(image_response.content)
                print(f"Downloaded {len(pages)} pages.")


