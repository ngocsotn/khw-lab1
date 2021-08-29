import my_file_control
# import my_html
from requests_html import HTML
#import my_regex
import my_selenium
import my_request

SHOPEE_URL_SALE = my_file_control.read_json("url.json")["shopee"]
SHOPEE_URL_BASE = my_file_control.read_json("url.json")["shopee_base"]
TIKI_URL_SALE = my_file_control.read_json("url.json")["tiki"]
TIKI_URL_BASE = my_file_control.read_json("url.json")["tiki_base"]

# browser = my_selenium.browse_with_chrome(SHOPEE_URL_SALE)

# root = HTML(html=browser.page_source)
# test = root.find(".flash-sale-item-card-link", first=False)

# for item in test:
#     print(item.text)
#     print("link ", SHOPEE_URL_BASE+ item.attrs['href'])
#     print()

data_array = my_request.get_shopee_data_by_api("",["sale", "giảm giá", "%"], 35)
my_file_control.write_shopee_api_data_to_json("./records/", "secrect", data_array)

