import math
import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns


def visualize_floor(df):
    '''
    Visualize the attr of direction
    '''
    sns.set(palette="muted", color_codes=True)  
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  
    sns.set(font='Microsoft YaHei', font_scale=0.8)  
    ax = sns.countplot(x='floor', data=df)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=5, rotation=90)  

    plt.show()


def word_to_num(str):
    simple_punctuation = '[\" /,),(]'

    str = re.sub('[\u4e00-\u9fa5]', '', str)
    str = re.sub(simple_punctuation, '', str)

    return int(str)


def pre_floor(df):
    '''
    If total_floor == NAN, then set total_floor = 32
    If floor <= 10 or 1/3*(total_floor), then floor = '低'
    If floor <= 20 or 2/3*(total_floor), then floor = '中'
    If floor > 20 or 2/3*(total_floor), then floor = '高'
    '''
    floor = df['floor'].tolist()
    total_floor = df['total_floor'].tolist()
    res_data = []
    
    for index, i in enumerate(floor):
        if i in ['低', '中', '高']:
            res_data.append(i)
        else:
            i = word_to_num(i)
            if math.isnan(total_floor[index]):     
                if i <= 10:
                    res_data.append('低')
                elif i <= 20:
                    res_data.append('中')
                else:
                    res_data.append('高')
            else:
                if i <= total_floor[index] / 3:
                    res_data.append('低')
                elif i <= 2 * (total_floor[index] / 3):
                    res_data.append('中')
                else:
                    res_data.append('高')

    df_res = pd.DataFrame(res_data)
    df['floor'] = df_res

    # if total_floor is NAN, then set total_floor = 32
    total_floor = [32 if math.isnan(x) else x for x in total_floor]
    df_res = pd.DataFrame(total_floor)
    df['total_floor'] = df_res

    return df


# if __name__ == '__main__':
#     fname = r'./data/backup.csv'
#     df = pd.read_csv(fname) 
#     df = visualize_floor(df, 'floor')
#     # df = pre_floor(df)
#     # print(df['floor'].value_counts())
#     # print(df['total_floor'].value_counts())
