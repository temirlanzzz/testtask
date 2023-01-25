import requests
from bs4 import BeautifulSoup
import json

URL = "https://shop.kz/smartfony/"

def get_json_data():
    response = requests.get(URL, headers={"Content-Type":"text/html; charset=utf-8", "User-Agent" : "Chrome/51.0.2704.103"})
    
    soup = BeautifulSoup(response.text, 'html.parser')
    last_page_number = soup.find('div', class_='bx-pagination-container row').find_all('li')[-2].text # сколько страниц есть 
    json_data = []
    current_page_number=1 
    while(current_page_number <= int(last_page_number)):
        phones = soup.find_all('div', class_='bx_catalog_item')
        for phone in phones:
            phone_text = phone.find('h4', class_='bx_catalog_item_title_text').text
            phone_articul = phone.find('div', class_='bx_catalog_item_XML_articul').text
            phone_articul = phone_articul.split()[-1]
            try:
                phone_price = phone.find_all('span', class_ = 'bx-more-price-text')[-1].text
            except IndexError:
                break
            phone_price= phone_price[:-1]
            phone_price = phone_price.replace(" ","")
            # phone_memory = phone.find_all('span', class_ = 'bx_catalog_item_value')[4].text
            phone_memory_texts = phone.find_all('span', class_ = 'bx_catalog_item_prop')
            counter = 0
            for phone_memory_text in phone_memory_texts:
                if phone_memory_text.text == 'Объем встроенной памяти:':
                    break
                else:
                    counter+=1
            phone_memory = phone.find_all('span', class_ = 'bx_catalog_item_value')[counter].text
            phone_data = {
                        "name": phone_text,
                        "articul": phone_articul,
                        "price": phone_price,
                        "memory-size": phone_memory
                        }
            json_data.append(phone_data)

        
        current_page_number+=1
        next_page_url = "https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/?PAGEN_1="+str(current_page_number)
        response = requests.get(next_page_url, headers={"Content-Type":"text/html; charset=utf-8", "User-Agent" : "Chrome/51.0.2704.103"})
        soup = BeautifulSoup(response.text, 'html.parser')
        

    with open('smartphones.json', 'w', encoding='utf-8') as f:
        s=json.dumps( json_data, ensure_ascii=False)
        f.write(s)