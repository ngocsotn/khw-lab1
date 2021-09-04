import requests

def get_shopee_data_by_api(SHOPEE_API_URL, keywords_array, limit):
    data = []
    for keyword in keywords_array:
        PARAMS_DICT = {
            "keywords": keyword,
            "limit": limit
        }
        response = requests.get(url= SHOPEE_API_URL, params=PARAMS_DICT)
        data.extend(response.json()["ListProductItem"])

    return data

def get_tiki_sale_list_by_api(TIKI_LIST_API_URL, cookies_dict, TIKI_API_HEADERS, page_number, limit):
    PARAMS_DICT = {
        "page": page_number,
        "tag_id": "best_deals",
        "per_page": limit
        # "time_id": 4
    }

    response = requests.get(url=TIKI_LIST_API_URL, cookies=cookies_dict, headers=TIKI_API_HEADERS, params=PARAMS_DICT)
    
    return response.json()

def get_tiki_sale_item_by_api(TIKI_ITEM_API_URL, cookies_dict, TIKI_API_HEADERS, master_id, item_id):
    NEW_URL = TIKI_ITEM_API_URL + master_id
    PARAMS_DICT = {
        "platform": "web",
        "spid" : item_id
    }

    response = requests.get(url=NEW_URL, cookies=cookies_dict, headers=TIKI_API_HEADERS, params=PARAMS_DICT)
    
    return response.json()