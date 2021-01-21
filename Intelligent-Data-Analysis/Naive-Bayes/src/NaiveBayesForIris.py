import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.metrics import confusion_matrix

def predict(X,X_class_dic,mean,std):
    p_2=posterior(X,X_class_dic[2],X_train_mean[2],X_train_std[2]) 
    p_1=posterior(X,X_class_dic[1],X_train_mean[1],X_train_std[1])
    p_0=posterior(X,X_class_dic[0],X_train_mean[0],X_train_std[0])
    return 1*(p_1>p_0) + 1*(p_2>p_1) - 0*(p_0>p_2)

def posterior(X,X_train_class,mean,std):
    product=np.prod(likelyhood(X,mean,std),axis=1)
    product=product*(X_train_class.shape[0]/X_train.shape[0])
    return product

def likelyhood(x, mean, sigma):
    return np.exp(-(x-mean)**2/(2*sigma**2))*(1/(np.sqrt(2*np.pi)*sigma))


Data=pd.read_csv('examples/iris.csv')

Data = Data.sample(frac = 1)
X = Data.iloc[:,:2].values
X = X.astype(float)
Y = Data.iloc[:,4].values

train_size = int(0.7*Data.shape[0])
test_size = int(0.3*Data.shape[0])
print('Размер обучающей выборки: ', str(train_size))
print('Размер тестовой выборки: ', str(test_size))

X_train = X[0:train_size, :]
Y_train = Y[0:train_size]

X_test = X[train_size:, :]
Y_test = Y[train_size:]

data_classes={}
data_classes[0]=np.array([[]])
data_classes[1]=np.array([[]])
data_classes[2]=np.array([[]])
first_two=True
first_one=True
first_zero=True

for i in range(Y_train.shape[0]):
    X_temp=X_train[i,:].reshape(X_train[i,:].shape[0],1)
    if Y_train[i]==2:
        if first_two==True:
            data_classes[2]=X_temp
            first_two=False
        else:
            data_classes[2]=np.append(data_classes[2],X_temp,axis=1)
    elif Y_train[i]==1:
        if first_one==True:
            data_classes[1]=X_temp
            first_one=False
        else:
            data_classes[1]=np.append(data_classes[1],X_temp,axis=1)
    elif Y_train[i]==0:
        if first_zero==True:
            data_classes[0]=X_temp
            first_zero=False
        else:
            data_classes[0]=np.append(data_classes[0],X_temp,axis=1)
         
data_classes[0] = data_classes[0].T
data_classes[1] = data_classes[1].T
data_classes[2] = data_classes[2].T
class0_count = data_classes[0].shape[0]
class1_count = data_classes[1].shape[0]
class2_count = data_classes[2].shape[0]
total_count = X_train.shape[0]

X_train_mean = []    
X_train_mean.append(np.mean(data_classes[0],axis=0))
X_train_mean.append(np.mean(data_classes[1],axis=0))
X_train_mean.append(np.mean(data_classes[2],axis=0))

X_train_std = []
X_train_std.append(np.std(data_classes[0],axis=0))
X_train_std.append(np.std(data_classes[1],axis=0))
X_train_std.append(np.std(data_classes[2],axis=0))


Y_pred = predict(X_test, data_classes, X_train_mean,X_train_std)
    
conf_matrix=confusion_matrix(Y_test,Y_pred)
print('Матрица ошибок:\n', conf_matrix)


TARGET_NAMES = ['setosa', 'versicolor', 'virginica']
COLORS = ['white', 'pink', 'red']

X_set, Y_set = X_train, Y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.5, stop = X_set[:, 0].max() + 0.5, step = 0.5), np.arange(start = X_set[:, 1].min() - 0.5, stop = X_set[:, 1].max() + 0.5, step = 0.5))
Z = predict(np.array([X1.ravel(), X2.ravel()]).T, data_classes, X_train_mean, X_train_std)
plt.subplot(121)
plt.contourf(X1, X2, Z.reshape(X1.shape), alpha = 1, cmap = cm.PuRd, extent = (X_set[:, 0].min() - 0.5, X_set[:, 0].max() + 0.5, X_set[:, 1].min() - 0.5, X_set[:, 1].max() + 0.5))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(Y_set)):
    plt.scatter(X_set[Y_set == j, 0], X_set[Y_set == j, 1], c = np.array(COLORS)[i], edgecolors = (0, 0, 0), label = TARGET_NAMES[j])
plt.title('Обучающая выборка')
plt.legend()

X_set, Y_set = X_test, Y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.5, stop = X_set[:, 0].max() + 0.5, step = 0.5),
                     np.arange(start = X_set[:, 1].min() - 0.5, stop = X_set[:, 1].max() + 0.5, step = 0.5))
Z = predict(np.array([X1.ravel(), X2.ravel()]).T, data_classes, X_train_mean, X_train_std)
plt.subplot(122)
plt.contourf(X1, X2, Z.reshape(X1.shape), alpha = 1, cmap = cm.PuRd, extent = (X_set[:, 0].min() - 0.5, X_set[:, 0].max() + 0.5, X_set[:, 1].min() - 0.5, X_set[:, 1].max() + 0.5))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(Y_set)):
    plt.scatter(X_set[Y_set == j, 0], X_set[Y_set == j, 1], c = np.array(COLORS)[i], edgecolors = (0, 0, 0), label = TARGET_NAMES[j])
plt.title('Тестовая выборка')
plt.legend()
plt.show()
