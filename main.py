import sys
sys.path.insert(0, 'src')
import my_file, controller

SHOPEE_URL= my_file.read_json("settings.json")["shopee"]
SHOPEE_URL_BASE = my_file.read_json("settings.json")["shopee_base"]
SHOPEE_API_URL = my_file.read_json("settings.json")["shopee_api"]
TIKI_URL = my_file.read_json("settings.json")["tiki"]
TIKI_URL_BASE = my_file.read_json("settings.json")["tiki_base"]
TIKI_LIST_API_URL = my_file.read_json("settings.json")["tiki_api_list"]
TIKI_ITEM_API_URL = my_file.read_json("settings.json")["tiki_api_item"]
TIKI_API_HEADERS = my_file.read_json("settings.json")["tiki_api_headers"]
FOLDER_NAME = my_file.read_json("settings.json")["folder_name"] + "/"

LIST_COMMANDS = ["all", "tiki", "shopee", "shopee-api"]
input_key = sys.argv

def run_all():
    print("start fetching/crawling all data from shopee, tiki, shopee-api...")
    if __name__ == '__main__' :
        try:
            controller.run_all_fetch(SHOPEE_URL, SHOPEE_URL_BASE, SHOPEE_API_URL, TIKI_URL, TIKI_URL_BASE, TIKI_LIST_API_URL, TIKI_ITEM_API_URL, TIKI_API_HEADERS)
        except:
            print("all broken...")

def run_shopee():
    print("start crawling only data from shopee...")
    try:
        controller.selenium_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)
    except:
        print("Something wrong when crawling shopee...")

def run_shopee_api():
    print("start fetching only data from shopee api...")
    try:
        controller.fetch_from_api_shopee(SHOPEE_API_URL)
    except:
        print("Something wrong when fetching api...")

def run_tiki():
    print("start crawling only data from tiki...")
    
    try:
        # controller.selenium_tiki_data(TIKI_URL, TIKI_URL_BASE)
        controller.continuous_request_tiki(TIKI_URL, TIKI_URL_BASE, TIKI_LIST_API_URL, TIKI_ITEM_API_URL, TIKI_API_HEADERS)
    except:
        print("Something wrong when crawling tiki...")

if len(input_key) != 2 or str(input_key[0]) != "main.py" or input_key[1] not in LIST_COMMANDS:
    print("command is invalid")
    print("command sample: python main.py X")
    print("X is one of these: all, tiki, shopee, shopee-api")
else:
    my_file.create_folder(FOLDER_NAME)
    controller.init_controller(FOLDER_NAME)
    print("...creating new json file...")
    if str(input_key[1]) == "shopee":
        run_shopee()
    elif str(input_key[1]) == "shopee-api":
        run_shopee_api()
    elif str(input_key[1]) == "all":
        run_all()
    elif str(input_key[1]) == "tiki":
        run_tiki()