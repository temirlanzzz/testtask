from fastapi import FastAPI
import json
app = FastAPI()

@app.get("/smartphones/")
def getItems(price:str):
    with open('smartphones.json', encoding='utf-8') as file:
        phones = json.load(file)
    filtered_phones=[]
    for phone in phones:
        if phone['price']==price:
            filtered_phones.append(phone)
    return filtered_phones