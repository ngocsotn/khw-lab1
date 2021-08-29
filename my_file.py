import json
import my_time

def generate_json_item():
    return {
        "number": "",
        "name": "",
        "price": "",
        "price_sale": "",
        "discount_percent": "",
        "sold_count":"",
        "link":"",
        "platform": "",
        "picture":[],
        "category":[],
        "point": "",
        "top_review": []
    }

def generate_json_mother(time_stamp, URL):
    data = {
        "count": "",
        "time": time_stamp,
        "url": URL,
        "data":[]
    }
    return data

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

def write_shopee_api_data_to_json(folder_name, URL, new_data_array, filename):
    current_time = my_time.get_current_time()
    file_name = folder_name + current_time + ".json"

    
    mother_data = generate_json_mother(current_time, URL)
    mother_data["count"] = 0
    mother_data["time"] = current_time
    mother_data["url"] = URL

    write_json(mother_data, file_name)
    
    count_child = 1
    for item in new_data_array:
        new_item = generate_json_item()
        new_item["number"] = count_child
        new_item["name"] = item["ProductName"]
        new_item["price"] = ""
        new_item["price_sale"] = item["SalePrice"]
        new_item["discount_percent"] = item["price_discount"]
        new_item["sold_count"] = "",
        new_item["link"] = item["LinkSEOWebsite"],
        new_item["picture"].append(item["ProductPreviewImage"])
        new_item["category"] = [],
        new_item["point"]  = "",
        new_item["top_review"] = [],
        new_item["platform"] = "shopee"
        count_child += 1

        append_json(new_item, file_name, "data")
        replace_data_json(count_child, file_name, "count")
