from pathlib import Path

import pandas as pd
import jsonlines
import json
import os
import sys

import datetime as dt

def getDataFromJson(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    
    dataFrame = pd.DataFrame(lines)
    dataFrame.columns = ['json_element']
    return pd.json_normalize(dataFrame['json_element'].apply(json.loads))
    
def jsonl_to_pd_dataframe(filepath):
    with jsonlines.open(filepath) as reader:
        data = [obj for obj in reader]

    return pd.DataFrame(data)

def get_merged_data():
    data_folder = Path("raw")
    products_path = data_folder / "products.jsonl"
    sessions_path = data_folder / "sessions.jsonl"
    products_df = getDataFromJson(products_path)
    sessions_df = getDataFromJson(sessions_path)

    sessions_df = pd.merge(sessions_df, products_df, how="left", on="product_id")

    return sessions_df

def add_purchase_attrib(data, df_group):
    last_event_log = df_group.iloc[-1].event_type
    is_purchased = last_event_log == 'BUY_PRODUCT'

    for index, row in df_group.iterrows():
        data.at[index, 'purchase'] = is_purchased


def add_time_specific_attribs(data, df_group):
    columns = df_group.columns
    session_date_start = df_group.iat[0, columns.get_loc('timestamp')]
    for index, row in df_group.iterrows():
        session_date_end = row.timestamp

        data.at[index, 'duration'] = (session_date_end - session_date_start).total_seconds()
        data.at[index, 'weekend'] = session_date_end.weekday() >= 5
        data.at[index, 'month'] = session_date_end.strftime("%m")
        data.at[index, 'weekday'] = int(session_date_end.weekday())
        data.at[index, 'hour'] = session_date_end.hour


def add_event_specific_attribs(data, df_group):
    total_viewed_items = 0
    product_set = set()

    columns = df_group.columns
    session_date_start = df_group.iat[0, columns.get_loc('timestamp')]
    for index, row in df_group.iterrows():
        session_date_end = row.timestamp
        minutes = (session_date_end - session_date_start).total_seconds() / 60.0

        total_viewed_items += 1
        product_set.add(row.product_id)

        data.at[index, 'unique_item_views'] = len(product_set)
        data.at[index, 'item_views'] = total_viewed_items
        data.at[index, 'click_rate'] = total_viewed_items / minutes if minutes != 0 else 0


def add_product_specific_attrib(data, df_group):
    unique_categories = set()
    for index, row in df_group.iterrows():
        main_category = row.category_path.split(';', 1)[0] if not pd.isna(row.category_path) else ''
        unique_categories.add(main_category)
        data.at[index, 'unique_categories'] = len(unique_categories)


def add_prev_session_specific_attrib(data):
    if len(data) == 0:
        return

    data.sort_values(['user_id', 'timestamp'], inplace=True)

    was_last_session_buying = False
    curr_session_buying = False

    current_session = data.at[0, 'session_id']
    current_user = data.at[0, 'user_id']
    for index, row in data.iterrows():
        if data.at[index, 'session_id'] != current_session:
            if data.at[index, 'user_id'] != current_user:
                current_user = data.at[index, 'user_id']
                was_last_session_buying = False
            else:
                was_last_session_buying = curr_session_buying
            current_session = data.at[index, 'session_id']

        data.at[index, 'last_session_purchase'] = was_last_session_buying
        curr_session_buying = data.at[index, 'purchase']


def add_new_attributes(data):
    for _, df_group in data.groupby('session_id'):
        add_time_specific_attribs(data, df_group)
        add_event_specific_attribs(data, df_group)
        add_product_specific_attrib(data, df_group)
        add_purchase_attrib(data, df_group)

    add_prev_session_specific_attrib(data)

def get_data():
    sessions = get_merged_data()
    sessions['timestamp'] = sessions['timestamp'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))

    add_new_attributes(sessions)

    columns_to_drop = ['product_id',
                       'purchase_id',
                       'timestamp',
                       'event_type',
                       'product_name',
                       'category_path']
    sessions = sessions.drop(columns_to_drop, axis=1)

    return sessions

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    if os.name == 'posix':
        DATA_PATH = module_path+"/data/raw/"
        DATASET_PATH = DATA_PATH+"/merged_sessions_products_data/"
    else:
        DATA_PATH = module_path+"\\data\\raw\\"
        DATASET_PATH = DATA_PATH+"\\merged_sessions_products_data\\"

if __name__ == "__main__":
    sessions = jsonl_to_pd_dataframe(DATA_PATH+'sessions.jsonl')
    users = jsonl_to_pd_dataframe(DATA_PATH+'users.jsonl')
    products = jsonl_to_pd_dataframe(DATA_PATH+'products.jsonl')
    merged = pd.merge(sessions, users, how="left", on="user_id")
    merged = pd.merge(merged, products, how="left", on="product_id")
    merged.drop(['street', 'name'], axis=1)
    # print(merged.head)
    merged.to_csv("merged_sessions_products_data", sep=' ', index=False)