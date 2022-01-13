from service import app, models, prediction_archive
from flask import request, abort


def predict(model):
    request_json = request.get_json().copy()
    attributes = models.get_model_attributes(request_json)

    prediction = model.predict(attributes)
    if len(prediction) == 0:
        abort(500, 'prediction failed')

    return bool(prediction[0])


@app.route('/predict/random_forest', methods=['GET', 'POST'])
def predict_random_forest():
    prediction = predict(models.random_forest_model)
    prediction_archive.insert_prediction(request.get_json(), prediction, "random_forest")

    return {
        "prediction": prediction,
        "model": "random_forest"
    }


@app.route('/predict/logistic_regression', methods=['GET', 'POST'])
def predict_logistic_reg():
    prediction = predict(models.logistic_reg_model)
    prediction_archive.insert_prediction(request.get_json(), prediction, "logistic_regression")

    return {
        "prediction": prediction,
        "model": "logistic_regression"
    }


@app.route('/predict/testAB', methods=['GET', 'POST'])
def predict_test_ab():
    user_id = request.get_json()['user_id']
    return predict_random_forest() if user_id % 2 else predict_logistic_reg()
