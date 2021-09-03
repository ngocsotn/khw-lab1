# WEB SCIENCE - PROJECT 1

## Members of the team
 - 20424027 - Phạm Thị Minh Hậu
 - 20424056 - Nguyễn Thế Ngọc
 - 20424058 - Nguyễn văn Nhật
---
## Project content
This app will crawl products that are on sale on tiki, shopee.
The information crawled like name, picture, discount percent, sale price, rating point...
This app also request API to fetch shopee data

## How to run
 - Must installed python 3 at least version 3.5 and make env path "python"
 - Must install these libraries before run:
    - **requests-html**
    - **selenium**
    - **requests_html**
 - Must installed Chrome browser, at least version 92.0
 - Run this command to crawl all data from shopee, tiki and request shopee api
 ```
    python main.py all
 ```
 - This command will crawl data only shopee or tiki:
 ```
    python main.py tiki

    or

    python main.py shopee

 ```
 - This command only request and fetch data from shopee api:
 ```
    python main.py shopee-api
 ```