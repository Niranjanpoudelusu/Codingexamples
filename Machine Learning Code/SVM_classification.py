# SVM

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

sns.set

# load data
train = pd.read_pickle(r"Kaggle\titanic\new_train.pkl")
test = pd.read_pickle(r"Kaggle\titanic\new_test.pkl")

# seed
rand_state = 1000

# split the data x, y
y_train = train['Survived']
X_train = train.drop('Survived', axis=1)
X_test = test.drop('PassengerId', axis=1)

# SVM classifier
SVM_classification = SVC(random_state=rand_state)
SVM_classification.fit(X_train, y_train)

# cross val 5 and 10 for checking accuracy
accuracy = cross_val_score(estimator=SVM_classification, X=X_train,
                           y=y_train, cv=5, scoring="accuracy")
accuracy = cross_val_score(estimator=SVM_classification, X=X_train,
                           y=y_train, cv=10, scoring="accuracy")

# Grid search
param_grid = {'C': [0.01, 0.1, 1, 10], 'gamma': [1, 0.1, 0.01, 'scale'], 'kernel': ['rbf', 'linear']}
grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=0, cv=5)
grid.fit(X_train, y_train)
grid.best_params_
grid.best_estimator_
SVM_final = SVC(C=1, kernel='rbf', gamma='scale', random_state=rand_state)

# accuracy with cross validation 5 and 10
accuracy = cross_val_score(estimator=SVM_final, X=X_train,
                           y=y_train, cv=5, scoring="accuracy")
accuracy = cross_val_score(estimator=SVM_final, X=X_train,
                           y=y_train, cv=10, scoring="accuracy")

# prediction
y_pred_test = SVM_final.fit(X_train, y_train).predict(X_test)
