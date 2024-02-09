from selenium import webdriver
from selenium.webdriver.common.by import By
from time import time


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options)
driver.get('https://orteil.dashnet.org/experiments/cookie/')

cookie = driver.find_element(By.ID, value='cookie')

items = driver.find_elements(By.CSS_SELECTOR, value='#store div')
price_ids = [item.get_attribute('id') for item in items]

timeout = time() + 5
five_mins = time() + 5*60

while True:
    cookie.click()

    if time() > timeout:

        all_prices = driver.find_elements(By.CSS_SELECTOR, value='#store b')
        items = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                items.append(cost)

        price_upgrades = {}
        for n in range(len(items)):
            price_upgrades[items[n]] = price_ids[n]

        money_element = driver.find_element(By.ID, value='money').text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in price_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        highest_price = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price]

        driver.find_element(By.ID, value=to_purchase_id).click()

        timeout = time() + 5

    if time() > five_mins:
        cookie_per_s = driver.find_element(By.ID, value='money').text
        print(cookie_per_s)
        break

