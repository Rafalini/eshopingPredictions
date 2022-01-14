import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def summarize_classification(y_test, y_pred):
    acc = accuracy_score(y_test, y_pred, normalize=True)
    prec = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    F1_score = f1_score(y_test, y_pred)

    return {'Accuracy:': acc,
            'Precision:': prec,
            'Recall:': recall,
            'F1_score:': F1_score}

def compare_result(result_dict):
    for key in result_dict:
        print('Classification:', key)

        print()
        print('Training data:')
        for score in result_dict[key]['training']:
            print(score, result_dict[key]['training'][score])

        print()
        print('Test Data:')
        for score in result_dict[key]['test']:
            print(score, result_dict[key]['test'][score])

        print()


def build_model(classifier_fn, dataset, onehot_cols=[], cols_to_drop=[], output_name='purchase',
                seed=116, test_frac=0.2, input=None, output=None):
    X_set = dataset.drop(output_name, axis=1)
    Y_set = dataset[output_name]

    X_set = pd.get_dummies(X_set, columns=onehot_cols)

    X_set = X_set.drop(cols_to_drop, axis=1)

    X_train, X_test, Y_train, Y_test = train_test_split(X_set, Y_set, test_size=test_frac, random_state=seed)

    if input is not None:
        with open(input, 'rb') as input_model:
            model = pickle.load(input_model)
    else:
        model = classifier_fn(X_train, Y_train)

    Y_pred = model.predict(X_test)
    Y_pred_train = model.predict(X_train)

    train_summary = summarize_classification(Y_train, Y_pred_train)
    test_summary = summarize_classification(Y_test, Y_pred)

    pred_result = pd.DataFrame({'y_test': Y_test, 'y_pred': Y_pred})

    conf_matrix = pd.crosstab(pred_result.y_pred, pred_result.y_test)
    
    if output is not None:
        with open(output, 'wb') as output_model:
            pickle.dump(model, output_model)
    
    return {'training': train_summary,
            'test': test_summary,
            'confusion_matrix': conf_matrix
            }
