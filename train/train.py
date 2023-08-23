import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RANSACRegressor
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn import metrics
from sklearn import preprocessing
from sklearn import datasets


def train_plot(y_test, y_pred):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  

    plt.figure(figsize=(15, 5))
    plt.plot(range(len(y_test)), y_test, 'r', label='test data')
    plt.plot(range(len(y_test)), y_pred, 'b', label='predictive data')
    plt.show()

    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
    plt.xlabel('test data')
    plt.ylabel('predictive data')
    plt.show()


def train_LR(df):
    df.drop(df.tail(1).index, inplace=True)

    # delete rows where unit_price > 150000
    # print(len(df[df['unit_price'] <= 150000]))
    # print(len(df[df['unit_price'] > 150000]))
    # print(len(df[df['unit_price'] > 150000])/len(df[df['unit_price'] <= 150000]))
    df = df[df['unit_price'] <= 150000]

    # smooth y
    # y = df['unit_price']
    y = np.log1p(df['total_price'])
    del df['unit_price']
    # df = preprocessing.scale(df)
    x = df
    # split train data and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
    print(x_train.shape)
    print(x_test.shape)

    lr = LinearRegression()
    # fit model
    lr.fit(x_train, y_train)  
    # print(lr.coef_)  
    # print(lr.intercept_) 
    y_pred = lr.predict(x_test)

    MSE = metrics.mean_squared_error(y_test, y_pred)
    RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    Rsquare = metrics.r2_score(y_test, y_pred)

    print("Train success! \nSome results :")
    print('MSE:', MSE)
    print('RMSE:', RMSE)
    print('Rsquare:', Rsquare)

    train_plot(y_test, y_pred)

    return df


def train_RANSAC(df):
    df.drop(df.tail(1).index, inplace=True)
    df = df[df['unit_price'] <= 150000]
    y = df['unit_price']
    del df['unit_price']
    x = df
    # split train data and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
    print(x_train.shape)
    print(x_test.shape)

    ransac = RANSACRegressor(LinearRegression(),
                            max_trials=88,
                            min_samples=66,
                            loss='squared_error',
                            residual_threshold=6)
    ransac.fit(x_train, y_train)
    # print(ransac.predict.coef_)  
    # print(ransac.predict.intercept_) 
    y_pred = ransac.predict(x_test)

    MSE = metrics.mean_squared_error(y_test, y_pred)
    RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    Rsquare = metrics.r2_score(y_test, y_pred)

    print("Train success! \nSome results :")
    print('MSE:', MSE)
    print('RMSE:', RMSE)
    print('Rsquare:', Rsquare)

    train_plot(y_test, y_pred)

    return df