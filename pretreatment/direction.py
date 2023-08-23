import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_direction(df):
    '''
    Visualize the attr of direction
    '''
    sns.set(palette="muted", color_codes=True)  
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  
    sns.set(font='Microsoft YaHei', font_scale=0.8)  
    ax = sns.countplot(x='direction', data=df)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=5, rotation=90)  
    plt.show()

    print(df['direction'].value_counts().head(50))


def pre_direction(df):
    '''
    If the direction includes '南', then direction == 1, otherwise direction == 0
    '''
    data = df.loc[:, 'direction']
    res_data = []

    for i in data:
        cnt = 0
        for tmp in i:
            # '南' =（\u5357）
            if tmp == '\u5357':
                cnt = cnt + 1
        if cnt >= 1:
            res_data.append(1)
        else:
            res_data.append(0)

    df_res = pd.DataFrame(res_data)
    df['direction'] = df_res

    return df



# if __name__ == '__main__':
#     fname = r'./data/backup.csv'
#     df = pd.read_csv(fname) 
#     visualize_direction(df)
#     df = pre_direction(df)
#     print(df)

