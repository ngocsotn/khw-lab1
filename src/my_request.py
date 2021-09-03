import requests

def get_shopee_data_by_api(SHOPEE_API_URL, keywords_array, limit):
    data = []
    for keyword in keywords_array:
        PARAMS = {
            "keywords": keyword,
            "limit": limit
        }
        response = requests.get(url= SHOPEE_API_URL, params=PARAMS)
        data.extend(response.json()["ListProductItem"])

    return data