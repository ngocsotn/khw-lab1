# WEB SCIENCE - PROJECT 1

## Members of the team
 - Phạm Thị Minh Hậu
 - Nguyễn Thế Ngọc
 - Nguyễn văn Nhật
---
## Project content
This app will crawl products that are on sale on tiki, shopee.
The information crawled like name, picture, discount percent, sale price, rating point...
This app also request API to fetch shopee data

## System requirements
- Having at least 8GB of RAM
- CPU Power at least have 2 Physical Cores, base Clock at least 2.4Ghz

## How to run
 - Must installed python 3 at least version 3.5 and make env path "python"
 - Must install these libraries before run:
    - **requests-html**
    - **selenium**

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
 
 
## All khw-lab (3 part):
-  [khw-lab1](https://github.com/ngocsotn/khw-lab1)
-  [khw-lab2](https://github.com/ngocsotn/khw-lab2)
-  [khw-lab3](https://github.com/ngocsotn/khw-lab3)
