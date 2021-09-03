from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# 1 vài cài đặt
scroll_await_time = 1
scroll_max_time = 1 #500
first_scroll_size = 180

selenium_drivers_downloads =  {
    "chrome": "https://sites.google.com/a/chromium.org/chromedriver/downloads",
    "edge": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/",
    "firefox": "	https://github.com/mozilla/geckodriver/releases",
    "safiri": "https://webkit.org/blog/6900/webdriver-support-in-safari-10/"
}

def set_scroll_max_time(new_value):
    global scroll_max_time
    scroll_max_time = new_value

def browse_with_chrome():
    browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
    browser.maximize_window()

    return browser

def scrolling_down_slowly(browser, height):
    for i in range(1, height, 5):
        browser.execute_script("window.scrollTo(0, window.scrollY + {});".format(i))
        time.sleep(0.05)

def browse_single_item(browser, URL, await_time):
    # mở tab mới
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
    browser.get(URL)
    time.sleep(await_time)
    scrolling_down_slowly(browser, 200)
    time.sleep(await_time)
    # đóng tab vừa mở
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
    return browser

def browse_scrolling_down(browser, loading_class_name):
    scroll_current_time = 0
    last_page_height = 1
    global scroll_max_time
    
    print("Scrolling down the website, please wait...")
    scrolling_down_slowly(browser, 200)

    while scroll_current_time < scroll_max_time:
        loading_element = browser.find_element_by_class_name(loading_class_name)
        if loading_element:
            scroll_current_time += 1

            if scroll_current_time >= scroll_max_time:
                break
            actions = ActionChains(browser)
            actions.move_to_element(loading_element).perform()
            scrolling_down_slowly(browser, 50)
            # print("Internet to slow, wait to loading")
            time.sleep(scroll_await_time *2 +1)
            
        if scroll_current_time >= scroll_max_time:
            break
        scroll_current_time += 1
        scrolling_down_slowly(browser, first_scroll_size)
        time.sleep(scroll_await_time)

        new_page_height = browser.execute_script("return document.body.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
    if scroll_current_time >= scroll_max_time:
        print("\nscroll max times in settings reached")
    else:
        print("\npage size maximum reached")
    
    return browser

def fetching_shopee(URL, await_time, loading_class_name):
    browser = browse_with_chrome()

    browser.get(URL)

    print("...await loading site for " + str(await_time) + " sec")
    time.sleep(await_time)

    browser = browse_scrolling_down(browser, loading_class_name)

    print("\nfetching data now...")

    return browser

def fetching_tiki(URL, await_time, ):
    browser = browse_with_chrome()

    browser.get(URL)

    print("...await loading site for " + str(await_time) + " sec")
    time.sleep(await_time)

    browser = browse_scrolling_down(browser, loading_class_name)

    print("\nfetching data now...")

    return browser