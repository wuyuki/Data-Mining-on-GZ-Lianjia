import pandas as pd

from pretreatment.pretreat import pretreatment
from train.train import train_LR
from train.train import train_RANSAC

if __name__ == '__main__':
    fname = r'./data/res.csv' #save data file after pretreatment
    df = pretreatment(fname)
    # df = pd.read_csv(fname) #read data directly if pretreatment is done before
    print(df)
    train_LR(df)
    # train_RANSAC(df)    