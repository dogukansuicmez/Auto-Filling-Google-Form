from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
#
CHROME_PATH = "C:\Development\chromedriver.exe"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdSEXcjpeKkaaS7GKxV0ktijGzbVHgir3Q1DvErwtFEORzQeQ/viewform?usp=sf_link"
URL_ZILLOW = "https://www.zillow.com/homes/for_rent/2-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.8563026328125%2C%22east%22%3A-122.0103553671875%2C%22south%22%3A37.491439942495816%2C%22north%22%3A38.05805731365078%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8"
}
response = requests.get(url=URL_ZILLOW,headers=headers)
response.raise_for_status()
content = response.text
soup = BeautifulSoup(content,"html.parser")

## getting addresses
adresses = soup.select("ul.photo-cards li address")
adress_list = []
for adress in adresses:
    adress_list.append(adress.getText())



## getting links
link_list = []
links = soup.select("ul.photo-cards li .list-card-top a")
for link in links:
    link_list.append(link.get("href"))

link_list[0] = "https://www.zillow.com/b/Emeryville-CA/37.836429,-122.29266_ll/" # It did come out in right way
# thts why i had to add wht Angela said in front of the partial link it yielded


## getting prices
price_list = []
prices = soup.select(".list-card-info .list-card-price")
for price in prices:
    price_list.append(price.getText())
price_list[0] = price_list[0].split("+")[0] # getting rid of the + sign from the first value
# getting rid of /mo from the rest of values in the list
for i in range(len(prices[1::])+1):
    price_list[i] = price_list[i].split("/")[0]


## lists of all required data
print(link_list)
print(price_list)
print(adress_list)


## waiting before it gets in to selenium part
time.sleep(4)

##### selenium part to auto fill google form
x_path_first = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
x_path_second = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
x_path_third = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
submit_button_x_path = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
driver = webdriver.Chrome(CHROME_PATH)
time.sleep(3)

## automatically writing process ##
for i in range(9):
    driver.get(url=GOOGLE_FORM)
    time.sleep(2)
    first = driver.find_element_by_xpath(x_path_first)
    time.sleep(2)
    first.send_keys(adress_list[i])
    time.sleep(2)
    second = driver.find_element_by_xpath(x_path_second)
    time.sleep(2)
    second.send_keys(price_list[i])
    time.sleep(2)
    third = driver.find_element_by_xpath(x_path_third)
    time.sleep(2)
    third.send_keys(link_list[i])
    time.sleep(2)
    sub_but = driver.find_element_by_xpath(submit_button_x_path)
    time.sleep(2)
    sub_but.click()
    time.sleep(5)
    if i == 8: # since i starts from 0 when it comes to 8, list's index comes to the end so it has to close the screen
        driver.quit()
