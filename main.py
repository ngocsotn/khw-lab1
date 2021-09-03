import controller
import my_file
import sys

SHOPEE_URL= my_file.read_json("url.json")["shopee"]
SHOPEE_URL_BASE = my_file.read_json("url.json")["shopee_base"]
SHOPEE_API_URL = my_file.read_json("url.json")["shopee_api"]
TIKI_URL = my_file.read_json("url.json")["tiki"]
TIKI_URL_BASE = my_file.read_json("url.json")["tiki_base"]

def run_all():
    print("start fetching data from all...")
    controller.analyze_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)
    controller.fetch_from_api_shopee(SHOPEE_API_URL)

def run_shopee():
    print("start crawling data from shopee...")
    controller.analyze_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)

def run_shopee_api():
    print("start fetching data from shopee api...")
    controller.fetch_from_api_shopee(SHOPEE_API_URL)

input_key = sys.argv
print(input_key[0])
if len(input_key) != 2 or str(input_key[0]) != "main.py":
    print("command is invalid")
    print("command sample: python main.py X")
    print("X is one of these: all, tiki, shopee, shopee-api")
else:
    if str(input_key[1]) == "shopee":
        run_shopee()
    elif str(input_key[1]) == "shopee-api":
        run_shopee_api()
    elif str(input_key[1]) == "all":
        run_all()