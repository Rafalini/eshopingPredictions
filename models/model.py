import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold
from sklearn.model_selection import RandomizedSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# from models import build_model, compare_result

sessions = pd.read_csv("../data/merged_sessions_products_data", sep=' ')

result_dict = {}

# print(sessions.head)
# print(sessions)

seed = 42
test_size = 0.1

X = sessions.drop('purchase', axis=1)
Y = sessions[['purchase']]

records_num = len(sessions)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

print('Size of entire dataset: ', records_num)
print('Size of training set: ', len(X_train))
print('Size of test set: ', len(X_test))

plt.rcParams['figure.figsize'] = [50, 50]
plt.rcParams.update({'font.size': 32})

train = pd.concat([X_train, Y_train], axis=1)

sns.heatmap(
    train.corr(method = 'spearman'),
    xticklabels = train.columns,
    yticklabels = train.columns,
    annot=True,
    fmt='0.1g'
)

list_one =[]
feature_ranking = SelectKBest(chi2, k=5)
fit = feature_ranking.fit(X_train, Y_train)

for i, (score, feature) in enumerate(zip(feature_ranking.scores_, X_train.columns)):
    list_one.append((score, feature))
    
dfObj = pd.DataFrame(list_one) 
dfObj = dfObj.sort_values(by=[0], ascending = False)

display(dfObj)

def logistic_fn_tuning(X_train, Y_train):
    # hyperparameters tuning
    model = LogisticRegression(max_iter=500)
    # define evaluation
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=seed)

    # define search space
    space = dict()
    space['solver'] = ['newton-cg', 'lbfgs', 'liblinear']
    space['penalty'] = ['l2']
    space['C'] = [100, 10, 1.0, 0.1, 0.01]

    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=seed)
    search = RandomizedSearchCV(model, space, scoring='accuracy', n_jobs=-1, cv=cv, random_state=seed)
    search.fit(X_train, Y_train)
    
    print(search.best_estimator_) # model = LogisticRegression(C=0.1, max_iter=500, solver='newton-cg')
    return search.best_estimator_

def logistic_fn(X_train, Y_train):
    model = LogisticRegression(C=0.1, max_iter=500, solver='newton-cg')
    model.fit(X_train, Y_train)
    
    return model

result_dict['Logistic Regression with corelated attributes'] = \
    build_model(logistic_fn, sessions, onehot_cols, dropped_cols_with_corelated_attr, 'purchase', seed, test_size)

result_dict['Logistic Regression without corelated attributes'] = \
    build_model(logistic_fn, sessions, onehot_cols, dropped_cols_without_corelated_attr, 'purchase', seed, test_size, output = './logistic_reg.pkl')
