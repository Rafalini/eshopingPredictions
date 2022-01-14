import pandas as pd
import json
import os
import sys


def splitCategories(products):
    maxLen = 0
    lis = ""
    for index, product in products.iterrows():
        if maxLen < len(product['category_path'].split(';')):
           maxLen = len(product['category_path'].split(';'))
           lis = product

    columns = products.columns
    for index, product in products.iterrows():
        categoryList = product[columns.get_loc('category_path')].split(';')
        for i in range(maxLen - len(categoryList)):
            categoryList.append("")
        for i in range(maxLen):
            categoryName = "cat_"+str(i)
            products[categoryName] = categoryList[i]

    print(products.head)
    products = products.drop('category_path', axis=1)
    print(products.head)

    return products


def getDataFromJson(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    
    dataFrame = pd.DataFrame(lines)
    dataFrame.columns = ['json_element']
    return pd.json_normalize(dataFrame['json_element'].apply(json.loads))


module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    if os.name == 'posix':
        DATA_PATH = module_path+"/data/raw/"
        DATASET_PATH = DATA_PATH+"/merged_sessions_products_data/"
    else:
        DATA_PATH = module_path+"\\data\\raw\\"
        DATASET_PATH = DATA_PATH+"\\merged_sessions_products_data\\"

if __name__ == "__main__":
    sessions = getDataFromJson(DATA_PATH+'sessions.jsonl')
    users = getDataFromJson(DATA_PATH+'users.jsonl')
    products = getDataFromJson(DATA_PATH+'products.jsonl')
    products = splitCategories(products)
    merged = pd.merge(sessions, users, how="left", on="user_id")
    merged = pd.merge(merged, products, how="left", on="product_id")
    merged.drop(['street', 'name'], axis=1)
    # print(merged.head)
    merged.to_csv("merged_sessions_products_data", sep=' ', index=False)