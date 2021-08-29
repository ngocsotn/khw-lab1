import requests

SHOPEE_API = "http://api.saledam.com/api/CheckSale/GetListDataByKeyWords"

def get_shopee_data_by_api(URL, keywords_array, limit):
    data = []
    for keyword in keywords_array:
        PARAMS = {
            "keywords": keyword,
            "limit": limit
        }
        response = requests.get(url= SHOPEE_API, params=PARAMS)
        data.extend(response.json()["ListProductItem"])
    
    return data