import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pretreatment.pretreat import pretreatment
from train.train import train_LR
from train.train import train_Ridge
from train.train import train_Ridge_get_param


if __name__ == '__main__':
    fname = r'./data/res.csv' #save data file after pretreatment
    # df = pretreatment(fname)
    df = pd.read_csv(fname) #read data directly if pretreatment is done before
    # print(df)

        # # checking the data if there is multicollinearity.
        # plt.figure(figsize=(15,7))
        # sns.heatmap(df.corr(),annot=True,cmap='viridis')
        # plt.show()

    # perform linear regression
    train_LR(df)  

    # perform ridge regression
    # train_Ridge_get_param(df)
    # train_Ridge(df)