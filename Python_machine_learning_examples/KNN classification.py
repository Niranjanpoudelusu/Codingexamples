# modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

sns.set

# load the pickles saved previously
train = pd.read_pickle(r"Kaggle\titanic\new_train.pkl")
test = pd.read_pickle(r"Kaggle\titanic\new_test.pkl")

# some info
train.head(5)
train.info()

# Splitting the data
y_train = train['Survived']
X_train = train.drop('Survived', axis=1)
X_test = test.drop('PassengerId', axis=1)

## KNN classification
# Fitting KNN classifier to th Training set, first simply using the number of neighbors as 5
KNN = KNeighborsClassifier(n_neighbors=5)
KNN.fit(X_train, y_train)

# coss validation 5 an 10
accuracy = cross_val_score(estimator=KNN, X=X_train,
                           y=y_train, cv=5, scoring='accuracy')
round(accuracy.mean(), 3)

# K = 10
accuracy = cross_val_score(estimator=KNN, X=X_train,
                           y=y_train, cv=10, scoring='accuracy')
round(accuracy.mean(), 3)

# Trying to get the number of neighbors

CV_error_rate = []
k = 50

for i in range(1, k):
    KNN_i = KNeighborsClassifier(n_neighbors=i)
    KNN_i.fit(X_train, y_train)
    MAE_i = -1 * cross_val_score(estimator=KNN_i, X=X_train,
                                 y=y_train, cv=5, scoring='neg_mean_absolute_error')
    CV_error_rate.append(np.mean(MAE_i))
K_value = pd.DataFrame({'CV_error_rates': CV_error_rate}, index=range(1, k))

# Plot the values
plt.figure(figsize=(10, 5))
sns.lineplot(data=K_value)
plt.title('Cross Validated Errors Rates VS K')
plt.xlabel('K')
plt.ylabel('Error rate')
plt.show()

# 10-fold cross-validation
CV_error_rate = []
k = 50

for i in range(1, k):
    KNN_i = KNeighborsClassifier(n_neighbors=i)
    KNN_i.fit(X_train, y_train)
    MAE_i = -1 * cross_val_score(estimator=KNN_i, X=X_train,
                                 y=y_train, cv=10, scoring='neg_mean_absolute_error')
    CV_error_rate.append(np.mean(MAE_i))

K_value = pd.DataFrame({'CV_error_rates': CV_error_rate}, index=range(1, k))

# plot
plt.figure(figsize=(10, 5))
sns.lineplot(data=K_value)
plt.title('Cross Validated Errors Rates VS K')
plt.xlabel('K')
plt.ylabel('Error rate')
plt.show()

# From figure k  =12 #for classification
KNN_updated = KNeighborsClassifier(n_neighbors=12)
KNN_updated.fit(X_train, y_train)

accuracy = cross_val_score(estimator=KNN_updated, X=X_train,
                           y=y_train, cv=5, scoring='accuracy')
error_rate = -1 * cross_val_score(estimator=KNN_updated, X=X_train,
                                  y=y_train, cv=5, scoring="neg_mean_absolute_error")

# 10-fold CV
accuracy = cross_val_score(estimator=KNN_updated, X=X_train,
                           y=y_train, cv=10, scoring='accuracy')
error_rate = -1 * cross_val_score(estimator=KNN_updated, X=X_train,
                                  y=y_train, cv=10, scoring="neg_mean_absolute_error")

#Prediction
y_pred_test = KNN_updated.predict(X_test)
