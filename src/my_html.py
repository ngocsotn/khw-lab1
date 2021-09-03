from requests_html import HTML

# def init_session():
#     return HTMLSession()

# def get_root_from_url(URL):
#     session = init_session()
#     return session.get(URL)

def parse_html(page_source):
    return HTML(html= page_source)

def shopee_all_items_im_sale_page(html_data):
    return html_data.find(".flash-sale-item-card-link", first=False)

def shopee_find_picture(html_data):
    picture = html_data.find(".flash-sale-item-card__animated-image", first=True)
    picture = picture.attrs['style']
    return picture[picture.index('http'):picture.index('")')]

def shopee_find_category_container(html_deep_data):
    container = html_deep_data.find(".container", first=False)
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
    for item in categories_raw:
        category.append(str(item.text))
    name = category.pop()

    return category, name

def shopee_find_price_sale_price_discount(html_deep_data):
    price = ""
    price_sale = ""
    discount = ""
    container = html_deep_data.find(".flex.flex-column > .flex.items-center", first=True)
    price_and_discount = container.text
    price_and_discount = price_and_discount.split()

    price = price_and_discount[0].replace("₫","")
    if len(price_and_discount) > 1:
        price_sale = price_and_discount[1].replace("₫","")
        discount = price_and_discount[2]
    
    return price, price_sale, discount

def shopee_find_point_and_sold(html_deep_data):
    point = "0"
    sold = "0"
    container = html_deep_data.find(".flex-auto.flex-column > .flex", first=True)
    start_and_sold = container.text 
    start_and_sold = start_and_sold.split()
    point = start_and_sold[0]
    sold = start_and_sold[4]
    #xử lý giá nếu có k
    exist_k = sold.count('k')
    if exist_k > 0:
        sold = sold.replace('k', '')
        sold = sold.replace(',','.')
        sold = str(float(sold) * 1000)

    if point == "Chưa":
        point = "0"
        
    return point, sold