import controller
import my_file

SHOPEE_URL= my_file.read_json("url.json")["shopee"]
SHOPEE_URL_BASE = my_file.read_json("url.json")["shopee_base"]
TIKI_URL = my_file.read_json("url.json")["tiki"]
TIKI_URL_BASE = my_file.read_json("url.json")["tiki_base"]

def main():
    print("crawling data")
    controller.analyze_shopee_data(SHOPEE_URL, SHOPEE_URL_BASE)

main()