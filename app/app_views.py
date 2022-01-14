from app import app, model_functions, sql_answers_archive
from flask import request, abort


def predict(model):
    request_json = request.get_json().copy()
    attributes = model_functions.get_model_attributes(request_json)

    answer = model.predict(attributes)
    if len(answer) == 0:
        abort(500, 'prediction failed')

    return bool(answer[0])


@app.route('/predict/rf', methods=['GET', 'POST'])
def give_prediction_random_forest():
    answer = predict(model_functions.random_forest_model)
    sql_answers_archive.insert_prediction(request.get_json(), answer, "random_forest")

    return {
        "prediction": answer,
        "model": "random_forest"
    }


@app.route('/predict/lr', methods=['GET', 'POST'])
def give_prediction_logistic_reg():
    answer = predict(model_functions.logistic_reg_model)
    sql_answers_archive.insert_prediction(request.get_json(), answer, "logistic_regression")

    return {
        "prediction": answer,
        "model": "logistic_regression"
    }


@app.route('/predict/AB', methods=['GET', 'POST'])
def give_prediction_test_ab():
    user_id = request.get_json()['user_id']
    return give_prediction_random_forest() if user_id % 2 else give_prediction_logistic_reg()
