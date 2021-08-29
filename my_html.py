from requests_html import *

def init_session():
    return HTMLSession()

def get_root_from_url(URL):
    session = init_session()
    return session.get(URL)

def start(URL):
    temp_url = "https://phongtro123.com" or URL

    root_data = get_root_from_url(temp_url)
    html_data = root_data.html
    text_data = root_data.text
    filter = ".post-item > .post-meta"
    tag_a = html_data.find(filter, first=False)
    for item in tag_a:
        tittle = item.find(".post-title > a", first=True).text
        print("tittle: ", tittle)

        link = item.find(".post-title > a", first=True).attrs['href']
        print("Link: ", temp_url+link)

        price = item.find(".post-price", first=True).text
        print("Price: ", price)

        acreage = item.find(".post-acreage", first=True).text
        print("acreage: ", acreage)

        location = item.find(".post-location > a", first=True).text
        print("location: ", location)

        time = item.find(".post-time", first=True).text
        print("time: ", time)

        summary = time = item.find(".post-summary", first=True).text
        print("summary: ", summary)   

        print()