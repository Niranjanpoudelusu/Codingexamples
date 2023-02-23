# modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA

sns.set()

# import saved data (we will apply principal component on train)
train = pd.read_pickle(r"titanic\new_train.pkl")

# info train
train.info()
train = train.drop('Survived', axis=1)
train.info()

# The data had scaled age (no need to do this but bringing data back to format)
train['Age'] = train['Age'] * 10
train['Fare'] = train['Fare'] * 100

train.describe().T

# Scaling feature space
sc = StandardScaler()
train = sc.fit_transform(train)

# apply PCA
pca = PCA(n_components=4)  ### Lets just take 4 components and try
pca.fit(train)
print(pca.components_)

print(pca.explained_variance_ratio_)

# looking at scree plot
pca = PCA(n_components=17)
pca.fit(train)

pca.explained_variance_ratio_

PVE = pd.DataFrame({'PVE': pca.explained_variance_ratio_,
                    'Principal Component': range(1, pca.n_components + 1)})
PVE.head()

# plot
plt.figure(figsize=(10, 10))
sns.lineplot(x='Principal Component', y='PVE', data=PVE)
plt.show()

# KERNEL PCA
### First lets try simple KernelPCa with 'rbf' kernel and 17 components with other values as default
kpca = KernelPCA(n_components=17, kernel='rbf')
K_train = kpca.fit_transform(train)

# looking at variance
Var = np.var(K_train, axis=0)
PVE = Var / np.sum(Var)
np.cumsum(PVE)
np.sum(Var)

# Looking ate Eigen value of components
kpca.lambdas_
Eig = pd.DataFrame({'eigen': kpca.lambdas_,
                    'Principal Component': range(1, kpca.n_components + 1)})
Eig.head()

# plot
plt.figure(figsize=(10, 10))
sns.lineplot(x='Principal Component', y='eigen', data=Eig)
plt.show()

# change the components number
kpca = KernelPCA(n_components=8, kernel='rbf')
K_train = kpca.fit_transform(train)
Var1 = np.var(K_train, axis=0)
PVE = Var1 / np.sum(Var)
len(kpca.alphas_)

kpca.lambdas_

### lets try with four components
kpca = KernelPCA(n_components=4, kernel='rbf')
K_train = kpca.fit_transform(train)
Var1 = np.var(K_train, axis=0)
PVE = Var1 / np.sum(Var)
PVE
