from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

selenium_drivers_downloads =  {
    "chrome": "https://sites.google.com/a/chromium.org/chromedriver/downloads",
    "edge": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/",
    "firefox": "	https://github.com/mozilla/geckodriver/releases",
    "safiri": "https://webkit.org/blog/6900/webdriver-support-in-safari-10/"
}

def scrolling_down_slowly(browser, height):
    for i in range(1, height, 10):
        browser.execute_script("window.scrollTo(0, window.scrollY + {});".format(i))
        time.sleep(0.03)

def browse_single_item(browser, URL, await_time):
    # browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
    # browser.maximize_window()
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
    browser.get(URL)
    # print("...await loading site for " + str(await_time) + " sec")
    # print("Scrolling down the website, please wait...")
    scrolling_down_slowly(browser, 400)
    time.sleep(await_time)
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
    return browser

def browse_with_chrome(URL, await_time):
    browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
    browser.maximize_window()
    browser.get(URL)
    print("...await loading site for " + str(await_time) + " sec")
    scroll_await_time = 1
    scroll_current_time = 0
    scroll_max_time = 1 #500
    scroll_size = 180
    last_page_height = 1
    
    time.sleep(await_time)
    print("Scrolling down the website, please wait...")
    scrolling_down_slowly(browser, 200)

    while True:
        if scroll_current_time >= scroll_max_time:
            break
        loading_element = browser.find_element_by_class_name('stardust-spinner__spinner')
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
        scrolling_down_slowly(browser, scroll_size)
        time.sleep(scroll_await_time)
        new_page_height = browser.execute_script("return document.body.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
    if scroll_current_time >= scroll_max_time:
        print("scroll max times in settings reached")
    else:
        print("Page size maximum reached")

    print("fetching data now...")
    return browser