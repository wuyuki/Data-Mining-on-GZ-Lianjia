import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.stats import probplot

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso, Ridge, RidgeCV
from sklearn.model_selection import RepeatedKFold, train_test_split
from sklearn import metrics
from sklearn import preprocessing

def train_line_plot(y_test, y_pred):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  

    plt.figure(figsize=(7, 5))
    plt.plot(range(len(y_test)), y_test, 'r', label='test data')
    plt.plot(range(len(y_test)), y_pred, 'b', label='predictive data')
    plt.show()


def train_scatter_plot(y_test, y_pred):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
    plt.xlabel('test data')
    plt.ylabel('predictive data')
    plt.show()


def train_historgram_of_residuals(y_test, y_pred):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  

    plt.figure(figsize=(7, 5))
    plt.hist(y_test - y_pred, bins=40)
    plt.xlabel('residuals')
    plt.ylabel('count')
    plt.show()


def train_q_q_plot(y_test, y_pred):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  

    plt.figure(figsize=(7, 5))
    probplot(y_test - y_pred, plot=plt);
    plt.show()


def train_plot(y_test, y_pred):
    train_line_plot(y_test, y_pred)
    train_scatter_plot(y_test, y_pred)
    train_historgram_of_residuals(y_test, y_pred)
    train_q_q_plot(y_test, y_pred)


def train_data(df):
    # prepare train and test data
    df = df[df['month'] == 9]
        #filter test data
        # print(len(df[(df['unit_price'] <= 150000) & (df['unit_price'] >= 25000)]))
        # print(len(df[(df['unit_price'] > 150000) | (df['unit_price'] < 25000)]))
        # print(len(df[(df['unit_price'] > 120000) | (df['unit_price'] < 0)])/len(df['unit_price']))
        # df = df[(df['unit_price'] <= 120000) & (df['unit_price'] >= 0)]
    y = df['unit_price']
        # smooth y
        # y = np.log1p(df['unit_price'])
    df = df.drop(columns=['total_floor', 'total_price', 'unit_price', 'month'])
        # df = preprocessing.scale(df)
    x = df
    # split train data and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
        # print(x_train.shape)
        # print(x_test.shape)

    return x_train, x_test, y_train, y_test


def train_result(y_test, y_pred):
    MSE = metrics.mean_squared_error(y_test, y_pred)
    RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    Rsquare = metrics.r2_score(y_test, y_pred)
    Adj_Rsquare = 1-((1 - Rsquare) * (len(y_test) - 1)/(len(y_test) - len(y_pred) - 1))
    print("Train success! \nSome results :")
    print('MSE:', MSE)
    print('RMSE:', RMSE)
    print('Rsquare:', Rsquare)
    print('Adj_Rsquare:', Adj_Rsquare)


def train_LR(df):
    x_train, x_test, y_train, y_test = train_data(df)
    # perform regression
    lr = LinearRegression()
    lr.fit(x_train, y_train)  
        # print(lr.coef_)  
        # print(lr.intercept_) 
    y_pred = lr.predict(x_test)
    # output result
    train_result(y_test, y_pred)
    # output plot
    train_plot(y_test, y_pred)


def train_Ridge_get_param(df):
    x_train, x_test, y_train, y_test = train_data(df)

    # perform regression
    alphas = [0.001, 0.01, 0.1, 1, 10]
    rcv = RidgeCV(alphas = alphas, store_cv_values = True)
    rcv.fit(x_train, y_train)
    print('Best Score: %s' % rcv.best_score_)
    print('Best Alpha: %s' % rcv.alpha_) 
    scores = rcv.cv_values_.mean(axis=0)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  
    plt.figure(figsize=(7, 5))
    plt.plot(alphas, scores)
    plt.show()


def train_Ridge(df):
    x_train, x_test, y_train, y_test = train_data(df)

    # perform regression
    rdg = Ridge(alpha = 0.1)
    rdg.fit(x_train, y_train)
    y_pred = rdg.predict(x_test)
    # output result
    train_result(y_test, y_pred)
    # output plot
    train_plot(y_test, y_pred)