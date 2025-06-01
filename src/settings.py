import json

def get_data_from_json() -> str:
    with open("data.json","r") as file:
            data = json.load(file)
            
            button_color = data["settings"]["button_color"]
            button_hover_color = data["settings"]["button_hover_color"]

            return button_color,button_hover_color
            
button_color,button_hover_color = get_data_from_json()

