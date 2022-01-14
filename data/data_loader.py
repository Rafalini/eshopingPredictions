import pandas as pd
import json
import os
import sys
import datetime

distanceDict = {'Radom' : 109, 'Kraków' : 294, 'Gdynia' : 372, 'Wrocław' : 384, 'Szczecin' : 566, 'Poznań' : 311, 'Warszawa' : 0}

def splitCategories(products):
    columns = products.columns
    for index, product in products.iterrows():
        categoryList = product[columns.get_loc('category_path')].split(';')
        for cat in categoryList:
            products[cat] = False

    for index, product in products.iterrows():
        categoryList = product[columns.get_loc('category_path')].split(';')
        for cat in categoryList:
            products.at[index, cat] = True

    return products


def formatTime(sessions):
    sessions['weekend'] = False
    #sessions['month'] = 0
    sessions['weekday'] = 0
    sessions['day'] = 0
    sessions['hour'] = 0
    for index, session in sessions.iterrows():
        sessionTime =  datetime.datetime.strptime(session['timestamp'], "%Y-%m-%dT%H:%M:%S")
        sessions.at[index, 'weekend'] = sessionTime.weekday() >= 5
        #sessions.at[index, 'month'] = sessionTime.strftime("%m")
        sessions.at[index, 'weekday'] = sessionTime.weekday()
        sessions.at[index, 'day'] = sessionTime.day
        sessions.at[index, 'hour'] = sessionTime.hour
    return sessions


def formatSessions(sessions):
    formatTime(sessions)
    return sessions.replace({'event_type': {'BUY_PRODUCT': True, 'VIEW_PRODUCT': False}})


def getDataFromJson(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    
    dataFrame = pd.DataFrame(lines)
    dataFrame.columns = ['json_element']
    return pd.json_normalize(dataFrame['json_element'].apply(json.loads))


def formatUsers(users):
    users['distance'] = 0
    for index, user in users.iterrows():
        users.at[index, 'distance'] = distanceDict[user['city']]
    return users

DATA_PATH = ""
DATASET_PATH = ""
module_path = os.path.abspath(os.path.join('..'))
if os.name == 'posix':
    DATA_PATH = module_path+"/data/raw/"
    DATASET_PATH = DATA_PATH+"/merged_sessions_products_data/"
else:
    DATA_PATH = module_path+"\\data\\raw\\"
    DATASET_PATH = DATA_PATH+"\\merged_sessions_products_data\\"

if __name__ == "__main__":
    sessions = formatSessions(getDataFromJson(DATA_PATH+'sessions.jsonl'))
    products = splitCategories(getDataFromJson(DATA_PATH+'products.jsonl'))
    users = formatUsers(getDataFromJson(DATA_PATH+'users.jsonl'))

    merged = pd.merge(sessions, users, how="left", on="user_id")
    merged = pd.merge(merged, products, how="left", on="product_id")
    merged = merged.drop(['street', 'city', 'name', 'category_path', 'purchase_id', 'timestamp', 'product_name'], axis=1)

    merged.to_csv("merged_sessions_products_data", sep=' ', index=False)