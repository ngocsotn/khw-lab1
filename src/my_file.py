import json
import my_time
from os import path, makedirs
import time

count_item = 0

def get_full_file_path(file_path):
    return path.abspath(file_path)

def check_exist(file_path):
    return path.exists(file_path)

def create_folder(folder_path):
    if not check_exist(folder_path):
        makedirs(folder_path)

def generate_json_item():
    return {
        "number": "",
        "name": "",
        "price": "",
        "price_sale": "",
        "discount_percent": "",
        "sold_count":"",
        "url":"",
        "platform": "",
        "picture":[],
        "category":[],
        "point": ""
    }

def generate_json_mother(time_stamp):
    data = {
        "count": "",
        "time": time_stamp,
        "data":[]
    }
    return data

def generate_new_record_file(folder_name):

    current_time = str(my_time.get_current_time())
    file_name = folder_name + current_time + ".json"
    mother_data = generate_json_mother(current_time)
    mother_data["count"] = 0
    mother_data["time"] = current_time

    write_json(mother_data, file_name)

    return file_name

def replace_data_json(new_data, filename, json_title):
    with open(filename, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data[json_title] = new_data
        file.seek(0)
        json.dump(file_data, file, indent = 4, ensure_ascii=False)

def append_json(new_data_json, filename, array_name):
    with open(filename, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data[array_name].append(new_data_json)
        file.seek(0)
        json.dump(file_data, file, indent = 4, ensure_ascii=False)
    
def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        return file_data

def write_json(new_data_json, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_data_json, file, indent = 4, ensure_ascii=False)

def write_single_item_to_json(item, file_path, platform):
    global count_item
    new_item = generate_json_item()
    new_item["number"] = count_item
    new_item["platform"] = platform

    if platform == "shopee-api":
        new_item["name"] = item["ProductName"]
        new_item["price_sale"] = item["SalePrice"].replace("đ", "")
        new_item["discount_percent"] = item["price_discount"]
        new_item["url"] = item["LinkSEOWebsite"]
        new_item["picture"].append(item["ProductPreviewImage"])

    else:
        new_item["name"] = item["name"]
        new_item["price"] = item["price"]
        new_item["price_sale"] = item["price_sale"]
        new_item["discount_percent"] = item["discount_percent"]
        new_item["sold_count"] = item["sold_count"]
        new_item["url"] = item["url"]
        new_item["picture"].extend(item["picture"])
        new_item["category"].extend(item["category"])
        new_item["point"]  = item["point"]
        
    count_item += 1

    append_json(new_item, file_path, "data")
    replace_data_json(count_item, file_path, "count")
    time.sleep(0.1)

def write_shopee_api_data_to_json(new_data_array, file_path):
    for item in new_data_array:
        write_single_item_to_json(item, file_path, "shopee-api")
