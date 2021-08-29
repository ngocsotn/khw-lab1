import my_request
import my_file
import my_selenium
from requests_html import HTML

# api
# data_array = my_request.get_shopee_data_by_api("",["sale", "giảm giá", "%"], 35)
# my_file.write_shopee_api_data_to_json("./records/", "secrect", data_array)

def analyze_shopee_data(URL, BASE_URL):
    browser = my_selenium.browse_with_chrome(URL, 5)
    root_data = HTML(html= browser.page_source)
    
    test = root_data.find(".flash-sale-item-card-link", first=False)
    print()
    length = len(test)
    print("data array size: " + str(length))

    for item in test:
        print(item.text)
        item_url = BASE_URL+ item.attrs['href']
        print("link ", item_url)
        item_browser = my_selenium.browse_single_item(browser, item_url, 2)
        item_data = HTML(html = item_browser.page_source)

        category = item_data.find(".aPKXeO", first=True)
        if category:
            print(category.text)
        
        print("")

    browser.close()