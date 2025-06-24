import json
from json_utils.settings import mangas_downloaded

def delete_data_in_json(value):
    # delete value
    with open("json_utils/data.json","r") as file:
        data = json.load(file)

    if value in data["user_var"]:
        del data["user_var"][f"{value}"]
    else:
        print(value,f" in {data["user_var"]} nicht gefunden")

    list_of_mangas_installed = []
    for key in mangas_downloaded:
        list_of_mangas_installed.append(key)

    # manga_data -> manga_title -> delete value
    target_value = value
    for key in data["manga_data"]:
        if data["manga_data"][key] == target_value:
            data["manga_data"][key] = list_of_mangas_installed[0]
            del list_of_mangas_installed
            print(f"{target_value} in ",data["manga_data"],"gelöscht")
        else:
            print("Nichts gefunden")


    # write file
    with open("json_utils/data.json","w") as file:
        json.dump(data,file,indent=4)


#delete_data_in_json("Solo Leveling")  Debug
