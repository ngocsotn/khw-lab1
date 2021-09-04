from os import replace
import my_file
import my_selenium
import my_request
import my_html

folder_name = "./records/"
file_path = ""
full_file_path = ""
shopee_loading_class = "stardust-spinner__spinner"
tiki_loading_class = "styles__LoaderWrapper-sc-1466pn8-1"

search_keywords = ["sale", "giảm", "giá", "ngay", "mua"]

my_selenium.set_scroll_max_time(1) #300


def init_controller(new_path):
    global folder_name, file_path, full_file_path
    folder_name = new_path
    file_path = my_file.generate_new_record_file(folder_name)
    full_file_path = my_file.get_full_file_path(file_path)

def fetch_from_api_shopee(SHOPEE_API_URL):
    global file_path

    print("\nstart requesting shopee api...")
    new_data_array = my_request.get_shopee_data_by_api(SHOPEE_API_URL, search_keywords, 100)
    
    print("fetched overview data size: " + str(len(new_data_array)))
    my_file.write_shopee_api_data_to_json(new_data_array, file_path)
    print("saved all data to " + full_file_path)

def analyze_shopee_data(URL, BASE_URL):
    global file_path
    global shopee_loading_class

    browser = my_selenium.fetching_shopee_tiki(URL, 5, shopee_loading_class)
    root_data = my_html.parse_html(browser.page_source)
    
    data_array = my_html.shopee_all_items_im_sale_page(root_data)
    length = len(data_array)
    print("\ncrawled overview data size: " + str(length))
    print("\nstart crawling details...")
    new_item = {}
    for item in data_array:
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
        print("\ncrawled a product details name: " + item_name)

        my_file.write_single_item_to_json(new_item, file_path, "shopee")

        print("saved data to " + full_file_path)
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

    browser.close()

def analyze_tiki_data(URL, BASE_URL):
    global file_path
    global tiki_loading_class

    browser = my_selenium.fetching_shopee_tiki(URL, 5, tiki_loading_class)
    root_data = my_html.parse_html(browser.page_source)
    data_array = my_html.tiki_all_items_im_sale_page(root_data)
    length = len(data_array)
    print("\ncrawled overview data size: " + str(length))
    print("\nstart crawling details...")
    new_item = {}
    for item in data_array:
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
        browser = my_selenium.browse_single_item(browser, item_url, 6)
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
        print("\ncrawled a product details name: " + item_name)

        my_file.write_single_item_to_json(new_item, file_path, "tiki")

        print("saved data to " + full_file_path)

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

    browser.close()
