# import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import sklearn.metrics
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

sns.set()

# read the data
data = pd.read_csv(r"nyc-rolling-sales_clean.csv")
seed_no = 1000

## For display purposes
pd.set_option('display.max_rows', 100)  # maximum number of rows the panda will display
pd.set_option('display.max_columns', 30)  # for the visualization of all the coluamns
data.head(5)

# Look at data
data.info()
data.describe(include='all')

# change types
categorical = ['BOROUGH', 'ZIP CODE', 'TAX CLASS AT TIME OF SALE']

for col in categorical:
    data[col] = data[col].astype("category")

# make some changes
data["Age"] = data["sale_year"] - data['YEAR BUILT']
data.head(5)

# Reduce some category types # Like grouping some categories into other
temp = data['BUILDING CLASS CATEGORY'].value_counts()
print(temp)

temp1 = temp[:6].index  # Getting top 6 values
data['BUILDING CLASS CATEGORY'] = data['BUILDING CLASS CATEGORY'].where(
    data['BUILDING CLASS CATEGORY'].isin(temp1), 'Other')

#
temp = data['TAX CLASS AT PRESENT'].value_counts()
temp1 = temp[:5].index  # Getting top 5 values
data['TAX CLASS AT PRESENT'] = data['TAX CLASS AT PRESENT'].where(
    data['TAX CLASS AT PRESENT'].isin(temp1), 'Other')

#
temp = data['BUILDING CLASS AT PRESENT'].value_counts()
temp1 = temp[:10].index  # Getting top 10 values
data['BUILDING CLASS AT PRESENT'] = data['BUILDING CLASS AT PRESENT'].where(
    data['BUILDING CLASS AT PRESENT'].isin(temp1), 'Other')

#
temp = data['BUILDING CLASS AT TIME OF SALE'].value_counts()
temp1 = temp[:10].index  # Getting top 10 values
data['BUILDING CLASS AT TIME OF SALE'] = data['BUILDING CLASS AT TIME OF SALE'].where(
    data['BUILDING CLASS AT TIME OF SALE'].isin(temp1), 'Other')

# making categorical
categorical = ['BUILDING CLASS CATEGORY', 'TAX CLASS AT PRESENT', 'BUILDING CLASS AT PRESENT',
               'BUILDING CLASS AT TIME OF SALE', 'sale_year', 'sale_month',
               'NEIGHBORHOOD']

for col in categorical:
    data[col] = data[col].astype("category")

# Look at data
data.describe(include='all')

# Drop variables we will not be using
data = data.drop(['NEIGHBORHOOD', 'ZIP CODE', 'YEAR BUILT', 'SALE DATE', 'sale_year'], axis=1)

# Data
data.info()

# Some plots to visualize data
plt.figure(figsize=(12, 5))
sns.distplot(data['SALE PRICE'], bins=30, rug=True)
plt.show()

# log transformation
plt.figure(figsize=(12, 5))
data['lSALE'] = np.log(data['SALE PRICE'])
sns.distplot(data['lSALE'], bins=30, rug=True)
plt.show()

data.drop('SALE PRICE', axis=1, inplace=True)

# Check correlations
plt.figure(figsize=(12, 10))
sns.heatmap(data.corr(), cmap='coolwarm', annot=True)
plt.show()

# Remove highly correlated variables
data.drop(['RESIDENTIAL UNITS', 'LAND SQUARE FEET', 'COMMERCIAL UNITS'], axis=1, inplace=True)

# Correlation
plt.figure(figsize=(12, 10))
sns.heatmap(data.corr(), cmap='coolwarm', annot=True)
plt.show()

# Checking variables in feature space
plt.figure(figsize=(12, 5))
sns.distplot(data['Age'], bins=30, color='r', rug=True)

print((data['Age'] > 150).sum())
data = data[data['Age'] < 150]  # remove some outliers

# Log transformation of age variable # There are some zeros make them 1
plt.figure(figsize=(12, 5))
data['lage'] = np.log(data['Age'] + 1)

# plot
sns.distplot(data['lage'], bins=30, rug=True)
plt.show()

data.drop('Age', axis=1, inplace=True)

# Area
plt.figure(figsize=(12, 5))
sns.distplot(data['GROSS SQUARE FEET'], bins=30, color='r', rug=True)

# Some outliers and general data cleaning
data = data[data['GROSS SQUARE FEET'] > 200]
print((data['GROSS SQUARE FEET'] > 50000).sum())
data = data[data['GROSS SQUARE FEET'] < 50000]

# plot
plt.figure(figsize=(12, 5))
data['lgross'] = np.log(data['GROSS SQUARE FEET'])
sns.distplot(data['lgross'], bins=30, rug=True)
plt.show()

data.drop('GROSS SQUARE FEET', axis=1, inplace=True)

# Units
plt.figure(figsize=(12, 5))
sns.distplot(data['TOTAL UNITS'], bins=30, color='r', rug=True)

print((data['TOTAL UNITS'] > 300).sum())

# outliers
data = data[data['TOTAL UNITS'] < 350]

# plot
plt.figure(figsize=(12, 5))
data['lunits'] = np.log(data['TOTAL UNITS'])
sns.distplot(data['lunits'], bins=30, rug=True)
plt.show()

# Create dummies for categorical
data = pd.get_dummies(data, drop_first=True)

# Defining variables and splitting the data
y = data['lSALE']
X = data.drop('lSALE', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed_no)

len(X_train) / len(X)

# Linear regression
sklearn_reg = LinearRegression()

# fit
sklearn_reg.fit(X_train, y_train)
sklearn_reg.predict(X_test)[0:4]

y_hat_test = sklearn_reg.predict(X_test)
log_predictions = pd.DataFrame({'Actuals': y_test, 'Predictions': y_hat_test})
predictions = np.exp(log_predictions)
predictions.head()

# Model
MSE_test = round(np.mean(np.square(predictions['Actuals'] - predictions['Predictions'])), 2)
RMSE_test = round(np.sqrt(MSE_test), 2)
R2 = sklearn_reg.score(X_train, y_train)

# MSE in logarithmic scale
y_hat_test1 = sklearn_reg.predict(X_test)
predictions1 = pd.DataFrame({'Actuals': y_test, 'Predictions': y_hat_test1})
predictions1.head()

MSE_test1 = round(np.mean(np.square(predictions1['Actuals'] - predictions1['Predictions'])), 6)
MSE_test1

RMSE_test1 = round(np.sqrt(MSE_test1), 6)
RMSE_test1

# Cross validation
model = LinearRegression()
NMSE = cross_val_score(estimator=model, X=X_test, y=y_test, cv=5, scoring="neg_mean_squared_error")
RMSE.mean()

# 10 fold
NMSE = cross_val_score(estimator=model, X=X_test, y=y_test, cv=10, scoring="neg_mean_squared_error")
RMSE = np.sqrt(-NMSE)
RMSE.mean()

# Cross-validation in trainset
NMSE = cross_val_score(estimator=model, X=X_train, y=y_train, cv=5, scoring="neg_mean_squared_error")
RMSE = np.sqrt(-NMSE)
RMSE.mean()

NMSE = cross_val_score(estimator=model, X=X_train, y=y_train, cv=10, scoring="neg_mean_squared_error")
RMSE = np.sqrt(-NMSE)
RMSE.mean()

# Non-linearity in fearture space
data = data.reset_index(drop=True)

X1 = data['lgross'].values
X1 = np.exp(X1)
y = data['lSALE']


# A function which returns the results
def poly_reg(poly_degree, X, y, test_size=0.2, rand_state=seed_no):
    poly_features = PolynomialFeatures(degree=poly_degree)

    X_poly = pd.DataFrame(poly_features.fit_transform(X.reshape(-1, 1)))
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=test_size, random_state=rand_state)

    poly_model = LinearRegression().fit(X_train, y_train)  # sm.OLS(y_train,X_train).fit()

    y_train_predicted = (
        poly_model.predict(X_train))  ## to get mse in normal scale use np.exp(poly_model.predict(X_train))
    y_test_predicted = (
        poly_model.predict(X_test))  ## to get mse in normal scale use np.exp(poly_model.predict(X_test))

    MSE_train = round(np.mean(np.square(y_train - y_train_predicted)), 2)
    RMSE_train = round(np.sqrt(MSE_train), 2)
    # R2_train = round(poly_model.rsquared,2)
    # Adj_R2_train = round(poly_model.rsquared_adj,2)

    ###Evaluating on test set
    MSE_test = round(np.mean(np.square(y_test - y_test_predicted)), 2)
    RMSE_test = round(np.sqrt(MSE_test), 2)

    return poly_degree, MSE_train, MSE_test, RMSE_train, RMSE_test


# call function
returns = []
for i in range(1, 9):
    returns.append(poly_reg(poly_degree=i, X=X1, y=y))
output = pd.DataFrame(returns, columns=['Degree', 'MSE_train', 'MSE_test', 'RMSE_train', 'RMSE_test'])
output['Rmse(tr-te)'] = output['RMSE_train'] - output['RMSE_test']
output

# Elbow method to see which degree is better

sns.lineplot(x='Degree', y='RMSE_train', data=output, color='g', label="Training RMSE")
plt.show()

# some more
sns.lineplot(x='Degree', y='RMSE_train', data=output, color='b', label="Training RMSE")
sns.lineplot(x='Degree', y='RMSE_test', data=output, color='r', label="Test RMSE")

# 5-fold cross validation
MSE_test = []
iterator = range(1, 8)
for i in iterator:
    poly_features = PolynomialFeatures(degree=i)
    X_poly = pd.DataFrame(poly_features.fit_transform(X1.reshape(-1, 1)))
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=233)
    poly_model = LinearRegression()  # sm.OLS(y_train,X_train).fit()
    NMSE = cross_val_score(estimator=poly_model, X=X_test, y=y_test, cv=5, scoring='neg_mean_squared_error')
    PMSE = -NMSE
    mean = PMSE.mean()
    lstn = [i, mean]
    MSE_test.append(lstn)
output = pd.DataFrame(MSE_test, columns=['Degree', 'MSE_test'])
output

# plots
sns.lineplot(x='Degree', y='MSE_test', data=output , color='b', label="Test MSE vs Polynomial Degree")
plt.show()

#RMSE
output["RMSE_test"] = np.sqrt(output['MSE_test'])

sns.lineplot(x='Degree', y='RMSE_test', data=output , color='b', label="Test MSE vs Polynomial Degree")
plt.show(

    

