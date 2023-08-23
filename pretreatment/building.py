import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_building(df):
    '''
    Visualize the attr of building
    '''
    df['building'] = df['building'].fillna('Unknown')
    sns.set(palette='muted', color_codes=True)  
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  
    sns.set(font='Microsoft YaHei', font_scale=0.8)  
    ax = sns.countplot(x='building', data=df)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=5, rotation=90)  
    plt.show()


def pre_building(df):
    '''
    Delete column('building') since nan has high proportion
    Replace nan value with the median value of built-year
    '''
    df = df.drop(columns=['building'])

    year_median = df['built_year'].median()
    df['built_year'] = df['built_year'].fillna(year_median)
    df['built_year'] = df['built_year'].astype('int64')
    df.loc[df['built_year'] > 2023, ['built_year']] = year_median
    df.loc[df['built_year'] < 1940, ['built_year']] = year_median

    return df


# if __name__ == '__main__':
#     fname = r'./data/backup.csv'
#     df = pd.read_csv(fname) 
#     df = visualize_building(df)
# #     df = pre_building(df)



