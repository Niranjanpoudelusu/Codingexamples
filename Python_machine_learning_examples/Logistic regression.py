# Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

sns.set()

# load data saved earlier
train = pd.read_csv(r"Kaggle\titanic\train.csv")
test = pd.read_csv(r"Kaggle\titanic\test.csv")

pd.set_option('display.max_rows', 100)  # maximum number of rows the panda will display
pd.set_option('display.max_columns', 30)  # for the visualization of all the columns

# Some look at the data
train.describe(include="all")
train.info()

# Separating title from name column
train['Title'] = train.Name.str.split(r'\s*,\s*|\s*\.\s*').str[1]

# reducing the number of categories
temp = train['Title'].value_counts()
temp1 = temp[:4].index  # Getting top 4 values
train['Title'] = train['Title'].where(train['Title'].isin(temp1), 'Other')
train['Title'].value_counts()

# Drop column because we have new columns
train = train.drop(['Name'], axis=1)

# Check the tickets
train['Tic'] = train.Ticket.str.split()  # Splitting ticket into two
train['len'] = train.Tic.str.len()
train['Tick'] = 0  # New column to add info

# Loop to assign the new columns with info from ticket
for i in range(len(train)):
    if train.iloc[i, 13] == 2:
        train.iloc[i, 14] = train.iloc[i, 12][0]
    else:
        train.iloc[i, 14] = 0

# There is extra dot or slash in some tickets,
# removing them so that same group of tickets can be matched.
train['Tick'] = train.Tick.str.replace('.', '')
train['Tick'] = train.Tick.str.replace('/', '')

# Some of them vary in case(lowercase and upper), so make all upper case
train['Tick'] = train.Tick.str.upper()

train.head(5)

### dropping the Ticket,Tic and len column which is further not required
train = train.drop(['Ticket', 'Tic', 'len', 'PassengerId'], axis=1)

train['Tick'].value_counts()  # Some information extracted from in front of the ticket

# Reduce the categories
train['Tick'] = train['Tick'].fillna('No_info')
tic_temp = train['Tick'].value_counts()
tic_temp1 = tic_temp[:4].index  # Getting top 3 values values from value counts

## Changing the non-frequent into other and reducing categories
train['Tick'] = train['Tick'].where(train['Tick'].isin(tic_temp1), 'Other')

# Visualize box plots
plt.figure(figsize=(10, 7))
sns.boxplot(x="Title", y="Age", data=train)
plt.show()

# Using title to assign missing age (from box plot recci)
## Filling the missing age values
train.loc[(train.Age.isnull()) & (train.Title == 'Mr'), 'Age'] = 33
train.loc[(train.Age.isnull()) & (train.Title == 'Mrs'), 'Age'] = 36
train.loc[(train.Age.isnull()) & (train.Title == 'Master'), 'Age'] = 5
train.loc[(train.Age.isnull()) & (train.Title == 'Miss'), 'Age'] = 22
train.loc[(train.Age.isnull()) & (train.Title == 'Other'), 'Age'] = 46

# Change the missing cabin to no_info
train['Cabin'] = train['Cabin'].fillna('No_info')
train.loc[(train.Cabin != 'No_info'), 'Cabin'] = 'Cabin'
train.head(50)

# Some more missing value imputations
train.loc[(train.Embarked.isnull()), 'Embarked'] = 'S'
test.describe(include="all")
test.info()

# same process for test
test['Title'] = test.Name.str.split(r'\s*,\s*|\s*\.\s*').str[1]

# keeping top frequent four categories and renaming other categories as other
temp = test['Title'].value_counts()
temp1 = temp[:4].index  # Getting top 4 values
test['Title'] = test['Title'].where(test['Title'].isin(temp1), 'Other')
test['Title'].value_counts()

# dropping the Name column which is further not required and passenger id as well
test = test.drop(['Name'], axis=1)

test['Tic'] = test.Ticket.str.split()
test['len'] = test.Tic.str.len()
test['Tick'] = 0

## For loop to assign the values to new column with this information of ticket
for i in range(len(test)):
    if test.iloc[i, 12] == 2:
        test.iloc[i, 13] = test.iloc[i, 11][0]
    else:
        test.iloc[i, 13] = 0

test['Tick'] = test.Tick.str.replace('.', '')
test['Tick'] = test.Tick.str.replace('/', '')
test['Tick'] = test.Tick.str.upper()

test['Tick'].value_counts()
test['Tick'] = test['Tick'].fillna('No_info')
test['Tick'] = test['Tick'].where(test['Tick'].isin(tic_temp1), 'Other')
test = test.drop(['Ticket', 'Tic', 'len'], axis=1)

plt.figure(figsize=(10, 7))
sns.boxplot(x="Title", y="Age", data=test)
plt.show()

test.loc[(test.Age.isnull()) & (test.Title == 'Mr'), 'Age'] = 29  # different from the filling in train set
test.loc[(test.Age.isnull()) & (test.Title == 'Mrs'), 'Age'] = 36
test.loc[(test.Age.isnull()) & (test.Title == 'Master'), 'Age'] = 5
test.loc[(test.Age.isnull()) & (test.Title == 'Miss'), 'Age'] = 22
test.loc[(test.Age.isnull()) & (test.Title == 'Other'), 'Age'] = 46

test['Cabin'] = test['Cabin'].fillna('No_info')
test.loc[(test.Cabin != 'No_info'), 'Cabin'] = 'Cabin'

# fare is missing in test
test['Fare'].mean()
test.loc[(test.Fare.isnull()), 'Fare'] = 35.60

# Change the type of variables
categorical = ['Pclass', 'Sex', 'Cabin', 'Embarked', 'Title', 'Tick']

for col in categorical:
    train[col] = train[col].astype("category")

categorical = ['Pclass', 'Sex', 'Cabin', 'Embarked', 'Title', 'Tick']

for col in categorical:
    test[col] = test[col].astype("category")

# Correlation
## lets look at the correlatiion for train set
sns.heatmap(train.corr(), cmap='coolwarm', annot=True)
plt.show()

### lets look at the correaltion for the test set
sns.heatmap(test.corr(), cmap='coolwarm', annot=True)
plt.show()

# rescale
train['Age'] = train['Age'] / 10
train['Fare'] = train['Fare'] / 100
test['Age'] = test['Age'] / 10
test['Fare'] = test['Fare'] / 100

# dummy variables
train = pd.get_dummies(train, drop_first=True)  ### Creating dummies for categorical variables
test = pd.get_dummies(test, drop_first=True)  ### Creating dummies for categorical variables

# split the data
y_train = train['Survived']
X_train = train.drop('Survived', axis=1)
X_test = test.drop('PassengerId', axis=1)

# model
logistic = LogisticRegression(solver='lbfgs')
logistic.fit(X_train, y_train)

# checking with cross validation
accuracy = cross_val_score(estimator=logistic, X=X_train,
                           y=y_train, cv=5, scoring="accuracy")  ### cross-flod k=5

round(accuracy.mean(), 2)

accuracy = cross_val_score(estimator=logistic, X=X_train,
                           y=y_train, cv=10, scoring="accuracy")  ### cross-flod k=10

round(accuracy.mean(), 2)

# Prediction
test_predictions = logistic.predict(X_test)
