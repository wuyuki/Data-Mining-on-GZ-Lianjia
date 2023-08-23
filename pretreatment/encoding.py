import pandas as pd

def encode_decoration(df):
    dummies = pd.get_dummies(df['decoration'])
    tmp = pd.concat([df, dummies], axis=1)
    del tmp['decoration']
    tmp.rename(columns={'精装': 'hardcover', '简装': 'simplicity', '毛坯':'rough', '其他': 'other'}, inplace=True)
    df = tmp
    return df

def encode_floor(df):
    dummies = pd.get_dummies(df['floor'])
    tmp = pd.concat([df, dummies], axis=1)
    del tmp['floor']
    tmp.rename(columns={'低楼层': 'low', '中楼层': 'medium', '高楼层': 'high'}, inplace=True)
    df = tmp
    return df

def encode_district(df):
    dummies = pd.get_dummies(df['district'])
    tmp = pd.concat([df, dummies], axis=1)
    del tmp['district']
    tmp.rename(columns={'白云': 'baiyun', 
                        '从化': 'conghua', 
                        '海珠': 'haizhu', 
                        '花都': 'huadou', 
                        '黄埔': 'huangpu',
                        '荔湾': 'liwan', 
                        '南沙': 'nansha', 
                        '番禺': 'panyu',
                        '天河': 'tianhe', 
                        '越秀': 'yuexiu',
                        '增城': 'zengcheng', 
                        }, inplace=True)
    df = tmp
    return df

def pre_encoding(df):
    df = encode_decoration(df)
    df = encode_floor(df)
    df = encode_district(df)
    return df

if __name__ == '__main__':
    fname = r'./data/backup.csv'
    df = pd.read_csv(fname) 
    df = pre_encoding(df)
    print(df)
