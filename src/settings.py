import json

def get_data_from_json() -> str:
    with open("data.json","r") as file:
            data = json.load(file)
            
            manga_name = data["manga_data"]["manga_title"]
            button_color = data["settings"]["button_color"]
            button_hover_color = data["settings"]["button_hover_color"]
            color_blue = data["settings"]["color_blue"]
            block_color = data["settings"]["block_color"]
            color_green = data["settings"]["color_green"]
            chapter_left = data["user_var"][f"{manga_name}"]

            return button_color,button_hover_color,block_color,color_blue,color_green,chapter_left,manga_name
            
button_color,button_hover_color,block_color,color_blue,color_green,chapter_left,manga_name = get_data_from_json()

