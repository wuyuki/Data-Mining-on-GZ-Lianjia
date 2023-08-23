import pandas as pd


def pre_model(df):
    '''
    Delete rows that the value of living room is not a number.
    Convert the type column('rooms') and column('living_rooms')
    '''
    df = df.loc[df['living_rooms'] != '室']

    return df


# if __name__ == '__main__':
#     fname = r'./data/backup.csv'
#     df = pd.read_csv(fname) 
#     df = pre_model(df)
#     print(df['rooms'].value_counts())
#     print(df['living_rooms'].value_counts())