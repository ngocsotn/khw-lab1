from selenium import webdriver
import time

selenium_drivers_downloads =  {
    "chrome": "https://sites.google.com/a/chromium.org/chromedriver/downloads",
    "edge": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/",
    "firefox": "	https://github.com/mozilla/geckodriver/releases",
    "safiri": "https://webkit.org/blog/6900/webdriver-support-in-safari-10/"
}

def browse_with_chrome(URL, await_time):
    browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
    browser.maximize_window()
    print("await loading site for" + str(await_time) + " s")
    browser.get(URL)
    time.sleep(await_time)
    print("fetching data now")
   
    # print(browser.page_source)
    return browser