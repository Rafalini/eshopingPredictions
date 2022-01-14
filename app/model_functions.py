import pickle

import pandas as pd
from flask import abort

with open('./models/random_forest.pkl', 'rb') as random_forest_pkl:
    random_forest_model = pickle.load(random_forest_pkl)

with open('./models/logistic_reg.pkl', 'rb') as logistic_reg_pkl:
    logistic_reg_model = pickle.load(logistic_reg_pkl)


def get_model_attributes(request_json):
    expected_json_attrib = ['user_id', 'offered_discount', 'price', 'duration', 'month', 'weekday', 'hour',
                            'click_rate', 'last_session_purchase']

    # check if map has expected keys
    if sorted(request_json.keys()) != sorted(expected_json_attrib):
        abort(400, 'expected json with fields: ' + str(expected_json_attrib) + ' got json with following fields:' +
              str(request_json.keys()))

    request_discount = request_json['offered_discount']
    for discount in range(0, 21, 5):
        request_json['offered_discount_' + str(discount)] = discount == request_discount

    request_month = request_json['month']
    for month in range(0, 12):
        request_json['month_' + str(month)] = month == request_month

    request_weekday = request_json['weekday']
    for weekday in range(0, 7):
        request_json['weekday_' + str(weekday)] = weekday == request_weekday

    request_json.pop('offered_discount')
    request_json.pop('weekday')
    request_json.pop('month')
    request_json.pop('user_id')

    model_attributes = pd.DataFrame(request_json, index=[0])

    dropped_cols = ['offered_discount_0', 'offered_discount_5', 'offered_discount_20',
                    "weekday_2", "weekday_3", "weekday_4", "weekday_5", "weekday_6",
                    "month_1", "month_5", "month_6", "month_9"]
    model_attributes = model_attributes.drop(columns=dropped_cols)

    return model_attributes
