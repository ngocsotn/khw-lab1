import my_file
import my_selenium
import my_request
import my_html
import threading
import time

# settings
folder_name = "./records/"
file_path = ""
full_file_path = ""
shopee_loading_class = "stardust-spinner__spinner"
tiki_loading_class = "styles__LoaderWrapper-sc-1466pn8-1"
shopee_prefix_log = "SHOPEE: "
shopee_api_prefix_log = "SHOPEE-API: "
tiki_prefix_log = "TIKI: "
tiki_cookies = {}
tiki_page = 1
tiki_limit = 24
tiki_max_product = 25

search_keywords = ["sale", "giảm", "giá", "ngay", "mua", "hot", "deal", "mã", "nhập", "kho"]

my_selenium.set_scroll_max_time(1) #300

# codes
def init_controller(new_path):
    global folder_name, file_path, full_file_path
    folder_name = new_path
    file_path = my_file.generate_new_record_file(folder_name)
    full_file_path = my_file.get_full_file_path(file_path)

def run_all_fetch(SHOPEE_URL, SHOPEE_URL_BASE, SHOPEE_API_URL, TIKI_URL, TIKI_URL_BASE, API_LIST, API_ITEM, TIKI_API_HEADERS):
    time.sleep(2)
    thread_shopee = threading.Thread(target= selenium_shopee_data, args=(SHOPEE_URL, SHOPEE_URL_BASE, ))
    thread_shopee_api = threading.Thread(target= fetch_from_api_shopee, args=(SHOPEE_API_URL,))
    thread_tiki = threading.Thread(target= continuous_request_tiki,args=(TIKI_URL, TIKI_URL_BASE, API_LIST, API_ITEM, TIKI_API_HEADERS))
    # thread_tiki = threading.Thread(target= selenium_tiki_data,args=(TIKI_URL, TIKI_URL_BASE,) )
    try:
        thread_shopee.start()
    except:
        print("Something wrong when crawling shopee...")

    try:
        time.sleep(0.5)
        thread_shopee_api.start()
    except:
        print("Something wrong when fetching api...")

    try:
        time.sleep(0.5)
        thread_tiki.start()
    except:
        print("Something wrong when crawling tiki...")

    thread_shopee_api.join()
    thread_shopee.join()
    thread_tiki.join()

def fetch_from_api_shopee(SHOPEE_API_URL):
    global file_path, shopee_api_prefix_log
    time.sleep(2)
    
    print()
    print(shopee_api_prefix_log + "start requesting shopee api...")
    new_data_array = my_request.get_shopee_data_by_api(SHOPEE_API_URL, search_keywords, 100)
    length = len(new_data_array)
    
    print(shopee_api_prefix_log + "fetched overview data size: " + str(length))
    my_file.write_shopee_api_data_to_json(new_data_array, file_path)
    print(shopee_api_prefix_log + "saved all data [" + str(length)+"] to " + full_file_path)

def selenium_shopee_data(URL, BASE_URL):
    time.sleep(2)
    global file_path, shopee_loading_class, shopee_prefix_log

    browser = my_selenium.fetching_shopee_tiki(URL, 5, shopee_loading_class, shopee_prefix_log)
    root_data = my_html.parse_html(browser.page_source)
    new_item = {}
    
    data_array = my_html.shopee_all_items_im_sale_page(root_data)
    length = len(data_array)
    print()
    print(shopee_prefix_log + "crawled overview data size: " + str(length))
    print(shopee_prefix_log + "start crawling details...")

    for i in range(length):
        item = data_array[i]
        item_url = BASE_URL + item.attrs['href']
        item_name = ""
        item_price = ""
        item_price_sale = ""
        item_discount_percent = ""
        item_sold_count = ""
        item_picture = []
        item_category = []
        item_point = ""

        # tìm url ảnh
        item_picture.append(my_html.shopee_find_picture(item))

        # đi chi tiết
        browser = my_selenium.browse_single_item(browser, item_url, 3)
        item_data = my_html.parse_html(browser.page_source)

        # tìm category
        container_main = my_html.shopee_find_category_container(item_data)
        
        # shopee chuyển đến trang nsx thay vì sản phẩm
        while(len(container_main.attrs['class']) != 1):
            deeper_link = my_html.shopee_find_deeper_link(item_data)
            item_url = BASE_URL + deeper_link.attrs['href']
            
            browser = my_selenium.browse_single_item(browser, item_url, 3)
            item_data = my_html.parse_html(browser.page_source)
            container_main = my_html.shopee_find_category_container(item_data)
        
        # lấy danh mục + tên
        item_category, item_name = my_html.shopee_find_category_and_name(container_main)

        #lấy giá + giá sale + tỷ lệ giảm + số đã bán
        item_price, item_price_sale, item_discount_percent = my_html.shopee_find_price_sale_price_discount(item_data)

        #lấy đánh giá sao trung bình + số đã bán
        item_point, item_sold_count = my_html.shopee_find_point_and_sold(item_data)
            
        # tạo item properties
        new_item["name"] = item_name
        new_item["price"] = item_price
        new_item["price_sale"] = item_price_sale
        new_item["discount_percent"] = item_discount_percent
        new_item["sold_count"] = item_sold_count
        new_item["url"] = item_url
        new_item["picture"] = item_picture
        new_item["category"] = item_category
        new_item["point"] = item_point
        print()
        print(shopee_prefix_log + "["+ str(i+1)+"/"+ str(length) +"] crawled a product details name: " + item_name)

        my_file.write_single_item_to_json(new_item, file_path, "shopee")

        print(shopee_prefix_log + "saved crawled data to " + full_file_path)
        # print("item_url: " + item_url)
        # print("item_category: "+ item_category[0] + ", " + item_category[1])
        # print("item_name: " + item_name)    
        # print("item_picture: " + item_picture[0])
        # print("item_price: " + item_price)
        # print("item_price_sale: " + item_price_sale)
        # print("item_discount_percent: " + item_discount_percent)
        # print("item_point: " + item_point)
        # print("item_sold_count: " + item_sold_count)
        # print()

    print(shopee_prefix_log + "finishing task...")
    browser.close()

# tạm không còn xài
def selenium_tiki_data(URL, BASE_URL):
    time.sleep(2)
    global file_path, tiki_loading_class, tiki_prefix_log
    new_item = {}

    browser = my_selenium.fetching_shopee_tiki(URL, 5, tiki_loading_class, tiki_prefix_log)
    root_data = my_html.parse_html(browser.page_source)
    data_array = my_html.tiki_all_items_im_sale_page(root_data)
    length = len(data_array)
    print()
    print(tiki_prefix_log + "crawled overview data size: " + str(length))
    print("TIKI: start crawling details...")

    for i in range(length):
        item = data_array[i]
        item_url = item.attrs['href']
        item_name = ""
        item_price = ""
        item_price_sale = ""
        item_discount_percent = ""
        item_sold_count = ""
        item_picture = []
        item_category = []
        item_point = ""

        #tìm url ảnh
        item_picture.append(my_html.tiki_find_picture(item))

        # đi sâu hơn
        browser = my_selenium.browse_single_item(browser, item_url, 4)
        item_data = my_html.parse_html(browser.page_source)

        # tìm container chứa tên + danh mục
        container_main = my_html.tiki_find_category_container(item_data)
        item_category, item_name = my_html.tiki_find_category_and_name(container_main)

        #lấy giá + giá sale + tỷ lệ giảm + số đã bán
        item_price, item_price_sale, item_discount_percent = my_html.tiki_find_price_sale_price_discount(item_data)

        #lấy số đã bán
        item_sold_count = my_html.tiki_find_sold(item_data)

        #lấy điểm đánh giá trung bình
        item_point = my_html.tiki_find_point(item_data)

        # tạo item properties
        new_item["name"] = item_name
        new_item["price"] = item_price
        new_item["price_sale"] = item_price_sale
        new_item["discount_percent"] = item_discount_percent
        new_item["sold_count"] = item_sold_count
        new_item["url"] = item_url
        new_item["picture"] = item_picture
        new_item["category"] = item_category
        new_item["point"] = item_point
        print()
        print(tiki_prefix_log + "["+ str(i+1)+"/"+ str(length) +"] crawled a product details name: " + item_name)

        my_file.write_single_item_to_json(new_item, file_path, "tiki")

        print(tiki_prefix_log + "saved crawled data to " + full_file_path)

        # print("item_url: " + item_url)
        # print("item_category: "+ item_category[0] + ", " + item_category[1])
        # print("item_name: " + item_name)    
        # print("item_picture: " + item_picture[0])
        # print("item_price: " + item_price)
        # print("item_price_sale: " + item_price_sale)
        # print("item_discount_percent: " + item_discount_percent)
        # print("item_point: " + item_point)
        # print("item_sold_count: " + item_sold_count)
        # print()
    
    print(tiki_prefix_log + "finishing task...")
    browser.close()

def get_tiki_cookies(URL, await_time):
    global file_path, tiki_prefix_log
    cookies = my_selenium.browse_get_all_cookies(URL, await_time, tiki_prefix_log)
    cookies_string = ""
    cookies_dict = {}

    for single_cookie in cookies:
        # cookies_string += single_cookie['name'] + '='+ single_cookie['value']+"; "
        cookies_dict[single_cookie['name']] = single_cookie['value']

    return cookies_dict

def handling_single_tiki_api_data(item, BASE_URL, API_ITEM, TIKI_API_HEADERS, tiki_current_product):
    global file_path, full_file_path, tiki_prefix_log, tiki_cookies, tiki_max_product
    new_item = {}
    new_item["picture"] = []
    new_item["category"] = []
    new_item["sold_count"]= ""

    # link
    new_item["url"] = BASE_URL + "/" + item["product"]["url_path"]

    # tên sp
    try:
        new_item["name"] = item["product"]["name"]
    except:
        new_item["name"] = ""

    # giá gốc
    try:
        new_item["price"] = str(item["product"]["list_price"])
    except:
        new_item["price"]= ""

    # giá sale
    try:
        new_item["price_sale"] = str(item["product"]["price"])
    except:
        new_item["price_sale"] = ""

    # % giảm giá
    try:
        new_item["discount_percent"] = str(item["discount_percent"])+"%"
    except:
        new_item["discount_percent"] = ""

    # điểm đánh giá trung bình
    try:
        new_item["point"] = str(round(item["product"]["rating_average"],1))
    except:
        new_item["point"] = ""

    item_id = str(item["product"]["id"])
    master_id = str(item["product"]["master_id"])

    details_data = my_request.get_tiki_sale_item_by_api(API_ITEM, tiki_cookies, TIKI_API_HEADERS, master_id, item_id)

    # danh mục
    try:
        categories_raw = details_data["productset_group_name"]
        categories_raw = categories_raw.split("/")
        new_item["category"].extend(categories_raw)
    except:
        new_item["category"] = []

    # hình ảnh
    try:
        picture_array = details_data["images"]
        for picture in picture_array:
            new_item["picture"].append(picture["base_url"])
    except:
        new_item["picture"] = []

    # số đã bán
    try:
        new_item["sold_count"] = str(details_data["all_time_quantity_sold"])
    except:
        new_item["sold_count"] = "0"

    print()
    print(tiki_prefix_log + "["+ str(tiki_current_product)+"/"+ str(tiki_max_product) +"] name: " + new_item["name"])
    my_file.write_single_item_to_json(new_item, file_path, "tiki")
    print(tiki_prefix_log + "saved data to " + full_file_path)

def continuous_request_tiki(URL, BASE_URL, API_LIST, API_ITEM ,TIKI_API_HEADERS):
    global tiki_prefix_log, tiki_limit, tiki_page, tiki_max_product, tiki_cookies
    tiki_current_product = 1
    tiki_cookies = get_tiki_cookies(URL, 5)
    print()
    print(tiki_prefix_log + "...creating new cookies")
    time.sleep(3)
    while(tiki_current_product < tiki_max_product):
        all_data = my_request.get_tiki_sale_list_by_api(API_LIST, tiki_cookies, TIKI_API_HEADERS, tiki_page, tiki_limit)
        array_data = all_data["data"]
        tiki_max_product = all_data["paging"]["total"]
        
        for item in array_data:
            if tiki_current_product % 500 == 0:
                print()
                print(tiki_prefix_log + "...please wait while we prepare new cookies")
                tiki_cookies = get_tiki_cookies(URL, 5)
                print()
                print(tiki_prefix_log + "...creating new cookies")
                time.sleep(4)
            handling_single_tiki_api_data(item, BASE_URL, API_ITEM, TIKI_API_HEADERS, tiki_current_product)
            time.sleep(0.01)
            tiki_current_product += 1

        tiki_page += 1
        time.sleep(1)

    print(tiki_prefix_log + "finishing task...")