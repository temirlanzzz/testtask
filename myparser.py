from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

URL = "https://shop.kz/smartfony/"
ELEMENT_LOCATOR = "//div[@class='bx_catalog_item']"
NAME_LOCATOR = ".//h4[@class='bx_catalog_item_title_text']"
ARTICUL_LOCATOR = ".//div[@class='bx_catalog_item_XML_articul']"
MEMORY_LOCATOR = ".//span[@class='bx_catalog_item_value']"
PRICE_LOCATOR = ".//span[@class='bx-more-price-text']"
LAST_PAGE_NUMBER_LOCATOR = ".//div[@class='bx-pagination-container row']//li"
NEXT_LOCATOR = "//li[@class='bx-pag-next']//a"

# collects data from shop.kz/ssmartfony/ and saves to smartphones.json
def get_json_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver =  webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(URL)
    json_data = []
    while(True):
        
        phones = driver.find_elements(by=By.XPATH, value=ELEMENT_LOCATOR)
        for phone in phones:
            phone_text = phone.find_element(by=By.XPATH, value = NAME_LOCATOR).text
            phone_articul = phone.find_element(by=By.XPATH, value = ARTICUL_LOCATOR).text
            phone_price = phone.find_elements(by=By.XPATH, value = PRICE_LOCATOR)[2].get_attribute("textContent")
            phone_price= phone_price[:-1]
            phone_price = phone_price.replace(" ","")
            phone_memory = phone.find_elements(by=By.XPATH, value = MEMORY_LOCATOR)[4].text
            
            json_data.append({
                        "name": phone_text,
                        "articul": phone_articul,
                        "price": phone_price,
                        "memory-size": phone_memory
                        })

        try:
            next_button=driver.find_element(by=By.XPATH, value=NEXT_LOCATOR)
            driver.execute_script("arguments[0].click();", next_button)
        except NoSuchElementException:
            break

    with open('smartphones.json', 'w', encoding='utf-8') as f:
        s=json.dumps( json_data, ensure_ascii=False)
        f.write(s)

    driver.quit()