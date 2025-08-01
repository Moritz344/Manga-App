import json

def write_data_to_json(main,key,new_value):
    try:

        with open("json_utils/data.json", "r") as file:
            content = json.load(file)


        if main in content:
            content[main][key] = new_value

        with open("json_utils/data.json","w") as file:
            json.dump(content,file,indent=4)


    except Exception as e:
        print(e)

def read_data_from_json(main,key):

    try:
        with open("json_utils/data.json","r") as file:
            content = json.load(file)

        return content[main][key]
    except Exception as e:
        print("Error in read_data_from_json",e)

