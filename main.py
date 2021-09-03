import sys
sys.path.insert(0, 'src')
import my_file, controller

SHOPEE_URL= my_file.read_json("settings.json")["shopee"]
SHOPEE_URL_BASE = my_file.read_json("settings.json")["shopee_base"]
SHOPEE_API_URL = my_file.read_json("settings.json")["shopee_api"]
TIKI_URL = my_file.read_json("settings.json")["tiki"]
TIKI_URL_BASE = my_file.read_json("settings.json")["tiki_base"]
FOLDER_NAME = my_file.read_json("settings.json")["folder_name"] + "/"

my_file.create_folder(FOLDER_NAME)
controller.init(FOLDER_NAME)

def run_all():
    print("start fetching/crawling all data from shopee, tiki, shopee-api...")
    controller.analyze_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)
    controller.fetch_from_api_shopee(SHOPEE_API_URL)

def run_shopee():
    print("start crawling only data from shopee...")
    controller.analyze_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)

def run_shopee_api():
    print("start fetching only data from shopee api...")
    controller.fetch_from_api_shopee(SHOPEE_API_URL)

def run_tiki():
    print("start crawling only data from tiki...")

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