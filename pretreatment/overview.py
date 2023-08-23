import pandas as pd
import sqlite3


def pre_rawdata():
    '''
    Get data from databse and back up the data as *.csv file
    '''
    # get data
    conn = sqlite3.connect('./data/data.sqlite')
    query = 'SELECT * FROM gz'
    df = pd.read_sql_query(query, conn)
    conn.close() 
    # save data
    fname = r'./data/backup.csv'
    df.to_csv(fname, encoding='utf-8', index=False) 
    return fname


def pre_overview():
    '''
    Get data information
    '''
    fname = pre_rawdata()
    df = pd.read_csv(fname)
    print(df.columns)
    print(df.shape)
    print(df.info())
    return df


# if __name__ == '__main__':
#     df = pre_overview()
#     print(df)