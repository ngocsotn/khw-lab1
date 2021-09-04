from requests_html import HTML

# def init_session():
#     return HTMLSession()

# def get_root_from_url(URL):
#     session = init_session()
#     return session.get(URL)

def parse_html(page_source):
    return HTML(html= page_source)

# Shopee
def shopee_all_items_im_sale_page(html_data):
    return html_data.find(".flash-sale-item-card-link", first=False)

def shopee_find_picture(html_data):
    picture = html_data.find(".flash-sale-item-card__animated-image", first=True)
    picture = ""
    if picture != None:
        picture = picture.attrs['style']
        picture = picture[picture.index('http'):picture.index('")')]
    return picture

def shopee_find_category_container(html_deep_data):
    container = html_deep_data.find(".container", first=False)
    container_main = ""
    if container != None:
        container_main = container[0]
        for consub in container:
            if len(consub.attrs['class']) == 1:
                container_main = consub
                break
    return container_main

def shopee_find_deeper_link(html_deep_data):
    return html_deep_data.find(".link-to-keep-parent-style", first=True)

def shopee_find_category_and_name(html_deep_data_container):
    category_wrap = html_deep_data_container.find(".flex.items-center", first=True)
    categories_raw = category_wrap.find("span", first=False)
    category = []
    name = ""
    if categories_raw != None :
        for item in categories_raw:
            category.append(str(item.text))
        name = category.pop()

    return category, name

def shopee_find_price_sale_price_discount(html_deep_data):
    price = ""
    price_sale = ""
    discount = ""
    container = html_deep_data.find(".flex.flex-column > .flex.items-center", first=True)

    if container != None:
        price_and_discount = container.text
        price_and_discount = price_and_discount.split()
        if len(price_and_discount) > 1:
            price = price_and_discount[0].replace("₫","")
            price_sale = price_and_discount[1].replace("₫","")
            discount = price_and_discount[2]
    
    return price, price_sale, discount

def shopee_find_point_and_sold(html_deep_data):
    point = "0"
    sold = "0"
    container = html_deep_data.find(".flex-auto.flex-column > .flex", first=True)
    if container != None:
        start_and_sold = container.text 
        start_and_sold = start_and_sold.split()
        if len(start_and_sold) > 4:
            point = start_and_sold[0]
            sold = start_and_sold[4]

        #xử lý giá nếu có k
        if sold.count('k') > 0:
            sold = sold.replace('k', '')
            sold = sold.replace(',','.')
            sold = str(float(sold) * 1000)

    if point == "Chưa":
        point = "0"
        
    return point, sold

# tiki
def tiki_all_items_im_sale_page(html_data):
    return html_data.find(".List__Wrapper-sc-1ap7nsk-0 > div > a", first=False)

def tiki_find_picture(html_data):
    picture = html_data.find("img", first=True)
    if picture != None:
        picture = picture.attrs['src']
    else:
        picture = ""

    return picture

def tiki_find_category_container(html_deep_data):
    container = html_deep_data.find(".Breadcrumb__Wrapper-sc-1a3qw0s-0 > .Container-sc-itwfbd-0", first=False)
    if len(container) != None:
        container_main = container[0]

    return container_main

# def tiki_find_deeper_link(html_deep_data):
#     return html_deep_data.find(".link-to-keep-parent-style", first=True)

def tiki_find_category_and_name(html_deep_data_container):
    # category_wrap = html_deep_data_container.find("", first=True)
    categories_raw = html_deep_data_container.find("a", first=False)
    category = []
    name = ""
    if categories_raw == None:
        return category, name

    for item in categories_raw:
        category.append(str(item.text))
    if len(categories_raw) > 1 :
        name = category.pop()
        category.pop(0) # trang chủ

    return category, name

def tiki_find_price_sale_price_discount(html_deep_data):
    price = ""
    price_sale = ""
    discount = ""
    container = html_deep_data.find(".flash-sale-price", first=True)
    if container == None:
        return "", "", ""

    price_and_discount = container.text
    price_and_discount = price_and_discount.split()
    if len(price_and_discount) > 2:
        price_sale = price_and_discount[0]
        price = (price_and_discount[2])[4:]
        discount = (price_and_discount[2])[1:4]

    return price, price_sale, discount

def tiki_find_sold(html_deep_data):
    sold = "0"
    container = html_deep_data.find(".below-title", first=True)

    if container == None:
        return sold

    start_and_sold = container.text 
    start_and_sold = start_and_sold.split()
    if(len(start_and_sold) > 6):
        sold = (start_and_sold[6]).replace('+','')
        
    return sold

def tiki_find_point(html_deep_data):
    point = "0"
    container = html_deep_data.find(".review-rating__point", first = True)

    if container == None:
        return point

    point_raw = container.text
    point_raw = point_raw.split()
    if len(point_raw) > 0:
        point = point_raw[0]

    return point