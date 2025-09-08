from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

GOOGLE_FORM = "https://forms.gle/gNCE32kpvAfRbPRR7"
ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(url=ZILLOW_CLONE)

zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")

#Scraping data from Renting Website

#Links
links = soup.find_all(name="a", class_="property-card-link")
link_list = []

for link in links:
    link_list.append(link.get("href").strip())

#Address
addresses = soup.find_all(name="address")
address_list = []

for address in addresses:
    address = address.text.split("\n")
    address_list.append(address[1].strip())

#Price
prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
prices_list = []

for price in prices:
    prices_list.append(price.text[0:6].strip()) # [0:6]- to split the string

#Using selenium to send data to Google Forms

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)

time.sleep(1)

#Filling the form

for i in range(len(link_list)):

    address_form = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_form.send_keys(address_list[i])

    price_form = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_form.send_keys(prices_list[i])

    link_form = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_form.send_keys(link_list[i])

    submit_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(0.5)

    next_form = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_form.click()