# Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

sns.set()

# Load data save previously
data = pd.read_pickle(r"machine learning\NYC_clean.pkl")

# random-seed
rand_state = 1000

# Look at data
data.info()

# Defining variables and splitting data
y = data['lSALE']
X = data.drop('lSALE', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=rand_state)

# Random forest without grid search
# Fitting Random Forests regression to the Training set
RF_regressor = RandomForestRegressor(n_estimators=100, max_features='sqrt')
RF_regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred_test = RF_regressor.predict(X_test)

predictions = pd.DataFrame({'y_actual_test': y_test,
                            'y_pred_test': y_pred_test,
                            'resid': y_test - y_pred_test})
predictions.head()

# MSE abd RMSE
MSE_test = round(np.mean(np.square(y_test - y_pred_test)), 2)
RMSE_test = round(np.sqrt(MSE_test), 2)

# Try to improve result with grid search
param_grid = {'n_estimators': [100, 1000, 1500],
              'max_features': ['sqrt', 'auto', 'log2'], 'max_depth': [5, 10, 20]}
grid = GridSearchCV(RandomForestRegressor(random_state=rand_state),
                    param_grid, refit=True, verbose=0, cv=5)
grid.fit(X_train, y_train)

# best values
grid.best_params_
y_pred_test_optimized = grid.predict(X_test)
MSE_test = round(np.mean(np.square(y_test - y_pred_test_optimized)), 2)
RMSE_test = round(np.sqrt(MSE_test), 2)

# Looking at feature importance
features = list(X_train.columns)

RF_regressor = RandomForestRegressor(n_estimators=1000,
                                     max_features='auto',
                                     max_depth=10, random_state=1000)
RF_regressor.fit(X_train, y_train)
y_hat = RF_regressor.predict(X_test)

MSE_test = round(np.mean(np.square(y_test - y_hat)), 2)
RMSE_test = np.sqrt(MSE_test)

importances = RF_regressor.feature_importances_

FIM = pd.DataFrame({'Features': features, 'Feature_importance': importances})
FIM = FIM.sort_values(by=['Feature_importance'])

# extract top 10
FIM = FIM.nlargest(10, ['Feature_importance'])

# plot
plt.figure(figsize=(10,6))
sns.barplot(y='Features', x='Feature_importance', data=FIM)
