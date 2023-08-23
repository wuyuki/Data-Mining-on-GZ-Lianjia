from datetime import date
from http.client import IncompleteRead
import platform
import random
import re
import sqlite3
import ssl
import time
import urllib.request, urllib.parse, urllib.error

import pandas as pd
from bs4 import BeautifulSoup


class WEBSPIDER:

    def get_suffixes(self, district):
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        proxies=urllib.request.ProxyHandler({'http':None})
        opener=urllib.request.build_opener(proxies)
        urllib.request.install_opener(opener)

        
        room_suffixes = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']
        floor_suffixes = ['lc1', 'lc2', 'lc3']
        lift_suffixes = ['ie1', 'ie2']
        pgs = []
        suffixes = []
        for room_suffix in room_suffixes:
            for floor_suffix in floor_suffixes:
                for lift_suffix in lift_suffixes:
                    suffix = lift_suffix + floor_suffix + room_suffix
                    url = 'https://gz.lianjia.com/ershoufang/{}/{}'.format(district, suffix)
                    try:
                        html = urllib.request.urlopen(url, context=ctx, timeout=30).read()
                    except (IncompleteRead) as e:
                        html = e.partial
                    soup = BeautifulSoup(html, 'lxml')    
                    total = soup.find('h2', class_='total fl').find('span').string
                    if int(total) > 3000:
                        pg = -1
                    elif int(total) == 0:
                        pg = 0
                    else:
                        pg_div = soup.find('div', class_ = 'page-box house-lst-page-box')
                        pg = json.loads(pg_div['page-data'])['totalPage']
                    suffixes.append(suffix)
                    pgs.append(pg)
        pg_suffix = {suffixes[i]: pgs[i] for i in range(len(suffixes))}
        return pg_suffix

    def get_district(self):
        districts = ['tianhe', 'yuexiu', 'liwan', 'haizhu', 'panyu', 'baiyun', 'huangpugz', 'nansha', 'conghua', 'zengcheng', 'huadou']
        suffixes = []
        for district in districts:
            suffix = self.get_suffixes(district)
            suffixes.append(suffix)
            print("sleep at %s" % time.ctime())
            time.sleep(random.randint(1,7) * 7)
            print("restart at %s" % time.ctime())
        district_suffix = {districts[i]: suffixes[i] for i in range(len(districts))}
        return district_suffix

    def get_url_list(self):
        url_list = []
        valid_list = []
        district_suffix = self.get_district()
        # district_suffix = {'tianhe': {'ie1lc1l1': 3, 'ie2lc1l1': -1, 'ie1lc2l1': 0}, 'yuexiu':  {'ie1lc1l1': 3, 'ie2lc1l1': 20, 'ie1lc2l1': 3}}
        for district, suffixes in district_suffix.items():
            for suffix, total_pg in suffixes.items():  
                if total_pg == -1 or total_pg == 0:
                    print('{} {} = {}'.format(district, suffix, total_pg))
                    continue         
                # generate page list
                pgs = list(range(1, total_pg + 1, 1))
                for pg in pgs:
                    url = 'https://gz.lianjia.com/ershoufang/{}/pg{}{}'.format(district, pg, suffix)
                    url_list.append(url)

        #save urls
        url_dict = {'url': url_list}
        url = pd.DataFrame(url_dict)
        if platform.system() == 'Windows':
            fname = r'C:\Users\yuki\Desktop\url_{}.csv'.format(date.today())
        elif platform.system() == 'Darwin':
            fname = r'/Users/yuki/Desktop/url_{}.csv'.format(date.today())
        url.to_csv(fname, encoding='utf-8', index=False)

        return url_list

    def get_apartment_data(self, url_list):
        '''
        Get basic information
        '''
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        proxies=urllib.request.ProxyHandler({'http':None})
        opener=urllib.request.build_opener(proxies)
        urllib.request.install_opener(opener)

        # new a dataframe
        df_list = []

        # loop over pages
        for index, url in enumerate(url_list):
            try:
                html = urllib.request.urlopen(url, context=ctx, timeout=30).read()
            except (IncompleteRead) as e:
                html = e.partial
            soup = BeautifulSoup(html, 'lxml')

            # get infomation from webpage
            listcontents = soup.find_all('li', class_='clear LOGVIEWDATA LOGCLICKDATA')
            title = [listcontent.find('div', class_='info clear').find('div', class_='title').find('a').string for listcontent in listcontents]
            region = [listcontent.find('div', class_='info clear').find('div', class_='flood').find_all('a')[0].string for listcontent in listcontents]
            position = [listcontent.find('div', class_='info clear').find('div', class_='flood').find_all('a')[1].string for listcontent in listcontents]
            house_info = [listcontent.find('div', class_='info clear').find('div', class_='address').find('div', class_='houseInfo').get_text() for listcontent in listcontents]
            follow_info = [listcontent.find('div', class_='info clear').find('div', class_='followInfo').get_text() for listcontent in listcontents]
            subway = [listcontent.find('div', class_='info clear').find('div', class_='tag').find('span', class_='subway') is None for listcontent in listcontents]
            taxfree = [listcontent.find('div', class_='info clear').find('div', class_='tag').find('span', class_='taxfree') is None for listcontent in listcontents]
            total_price = [listcontent.find('div', class_='info clear').find('div', class_='priceInfo').find('div', class_='totalPrice').find('span').string for listcontent in listcontents]
            reference = [listcontent.find('div', class_='info clear').find('div', class_='priceInfo').find('div', class_='totalPrice').find('i').string for listcontent in listcontents]
            unit_price = [listcontent.find('div', class_='info clear').find('div', class_='priceInfo').find('div', class_='unitPrice').find('span').string for listcontent in listcontents]
            district = re.findall('https://.*com/.*/(.*)/.*', url) * len(listcontents)
            obtained_date = [date.today().strftime('%Y-%m-%d')] * len(listcontents)


            df = pd.DataFrame(list(zip(title, region, position, house_info, follow_info, subway, taxfree, total_price, reference, unit_price, district, obtained_date)), columns=['title', 'region', 'position', 'house_info', 'follow_info', 'subway', 'taxfree', 'total_price', 'reference', 'unit_price', 'district', 'date'])
            df_list.append(df)

            if index % 7 == 0:
                print("index = %d, sleep at %s" %(index, time.ctime()))
                time.sleep(random.randint(1,7) * 7)
                print("index = %d, restart at %s" %(index, time.ctime()))
            if index % 100 == 0:
                print("index = %d, sleep at %s" %(index, time.ctime()))
                time.sleep(random.randint(1,7) * 7 * 7)
                print("index = %d, restart at %s" %(index, time.ctime()))
            
        output = pd.concat(df_list)
        print(output)
        if platform.system() == 'Windows':
            fname = r'C:\Users\yuki\Desktop\web_raw_data_{}.csv'.format(date.today())
        elif platform.system() == 'Darwin':
            fname = r'/Users/yuki/Desktop/web_raw_data_{}.csv'.format(date.today())
        output.to_csv(fname, encoding='utf-8', index=False)

        return output

    def clean_data(self, file):
        '''
        Clean data
        '''
        if platform.system() == 'Windows':
            fname = r'C:\Users\yuki\Desktop\{}.csv'.format(file)
        elif platform.system() == 'Darwin':
            fname = r'/Users/yuki/Desktop/{}.csv'.format(file)
        df = pd.read_csv(fname)

        #delete rows
        df = df[~df.house_info.str.contains('车位')]

        #clean data(title)
        df['keywords'] = [','.join(re.split(' |,', title)) for title in df['title']]

        #clean data (house_info)
        df['rooms'] = [info.split('|')[0].strip()[0] for info in df['house_info']]
        df['living_rooms'] = [info.split('|')[0].strip()[2] for info in df['house_info']]
        df['area'] = [info.split('|')[1].strip().replace('平米', '') for info in df['house_info']]
        df['direction'] = [','.join(re.split(' ', info.split('|')[2].strip())) for info in df['house_info']]
        df['decoration'] = [info.split('|')[3].strip() for info in df['house_info']]
        floor = [info.split('|')[4].strip().split('层')[0] for info in df['house_info']]
        df['floor'] = [i.replace('楼', '') for i in floor]
        total_floor = [info.split('|')[4].strip().split('层')[1] for info in df['house_info']]
        df['total_floor'] = [re.search(r'\d+', i).group(0) if '共' in i else None for i in total_floor]
        
        df['temp_str'] = [info.split('|')[5].strip() if len(info.split('|')) >= 6 else None for info in df['house_info']]
        build_year = []
        building = []
        for str in list(df['temp_str']):
            if str is None:
                build_year.append(None)
                building.append(None)
            elif len(str.split('|')) == 2:
                build_year.append(str.split('|')[0].strip().replace('年建', ''))
                building.append(str.split('|')[1].strip())
            elif len(str.split('|')) == 1:
                if '年' in str:
                    build_year.append(str.split('|')[0].strip().replace('年建', ''))
                    building.append(None)
                elif '楼' in str:
                    build_year.append(None)
                    building.append(str.split('|')[0].strip())
                else:
                    build_year.append(None)
                    building.append(None)
        df.insert(len(df.columns), 'built_year', build_year)
        df.insert(len(df.columns), 'building', building)

        # clean data(follow_info)
        follower = [info.split('/')[0].strip() if info is not None else None for info in df['follow_info']]
        df['follower'] = [re.search(r'\d+', i).group(0) if i is not None else None for i in follower]
        pub_date = [info.split('/')[1].strip() for info in df['follow_info']]
        df['pub_date'] = [i.replace('以前发布', '') for i in pub_date]

        #clean data(price)
        df['reference'] = [True if '参考价' in ref else False for ref in df['reference']]
        df['unit_price'] = [int(price.replace('元/平', '').replace(',', '')) for price in df['unit_price']]

        #clean district
        district_dict = {
            'baiyun': '白云',
            'conghua': '从化',
            'haizhu': '海珠',
            'huadou': '花都',
            'huangpugz': '黄埔',
            'liwan': '荔湾',
            'nansha': '南沙',
            'panyu': '番禺',
            'tianhe': '天河',
            'yuexiu': '越秀',
            'zengcheng': '增城',
        }
        df['district'] = [district_dict[key] for key in df['district']]

        #arrange df
        df.drop(columns=['title', 'house_info', 'temp_str', 'follow_info'])
        order = ['keywords', 'district', 'region', 'position', 'rooms', 'living_rooms', 'area', 'direction', 'decoration', \
                    'floor', 'total_floor', 'built_year', 'building', 'subway', 'taxfree', 'total_price','reference', 'unit_price', 'date']
        df = df[order]

        if platform.system() == 'Windows':
            fname = r'C:\Users\yuki\Desktop\{}_modified.csv'.format(file)
        elif platform.system() == 'Darwin':
            fname = fname = r'/Users/yuki/Desktop/{}_modified.csv'.format(file)
        df.to_csv(fname, encoding='utf-8', index=False)
        # print(df)
        return df

    def update_sql(self, df, database):
        '''
        Update each table
        '''
        # print(df)
        if df.empty:
            print('Failed to update table daily.')
            return
        conn = sqlite3.connect('data.sqlite')
        df.to_sql(database, con=conn, if_exists='append', index=False)
        conn.commit()
        conn.close() 

    def output_gz_data(self):
        '''
        Output total guangzhou table
        '''
        df_gz = pd.DataFrame()
        df_list =[]

        districts = {
            'baiyun': '白云',
            'conghua': '从化',
            'haizhu': '海珠',
            'huadou': '花都',
            'huangpugz': '黄埔',
            'liwan': '荔湾',
            'nansha': '南沙',
            'panyu': '番禺',
            'tianhe': '天河',
            'yuexiu': '越秀',
            'zengcheng': '增城',
        }

        conn = sqlite3.connect('data.sqlite')
        #tables = pd.read_sql('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";', con=conn)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        for table in tables:
            query = 'SELECT * FROM {}'.format(table[0])
            df = pd.read_sql_query(query, conn)
            df['district'] = districts[table[0]]
            df_list.append(df)
        df_gz = pd.concat(df_list)
        conn.close() 

        order = ['keywords', 'district', 'region', 'position', 'rooms', 'living_rooms', 'area', 'direction', 'decoration', \
                    'floor', 'total_floor', 'built_year', 'building', 'subway', 'taxfree', 'total_price','reference', 'unit_price']
        df_gz = df_gz[order]

        print(df_gz)
        if platform.system() == 'Windows':
            fname = r'C:\Users\yuki\Desktop\gz.csv'
        elif platform.system() == 'Darwin':
            fname = r'/Users/yuki/Desktop/gz.csv'
        df_gz.to_csv(fname, encoding='utf-8', index=False)

        return df_gz


web_spider = WEBSPIDER()
# # get url list
# web_spider.get_url_list()
# # get data from achieved urls
# url_file_name = 'url_2023-07-05'
# if platform.system() == 'Windows':
#     fname = r'C:\Users\yuki\Desktop\{}.csv'.format(url_file_name)
# elif platform.system() == 'Darwin':
#     fname = r'/Users/yuki/Desktop/{}.csv'.format(url_file_name)
# url_df = pd.read_csv(fname)
# url_list = url_df['url'].tolist()
# # get data from web
# df_house = web_spider.get_apartment_data(url_list)
# print(df_house)

#####################################################
# in general, we don't need this part below
#####################################################
# # in case block id, we have to split parts to get data sometimes
# # combine data since it was achieved several times
# df_list = []
# suffixes = ['500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500']
# for suffix in suffixes:
#     filename = r'C:\Users\yuki\Desktop\web raw data\web_raw_data_2023-05-08_{}.csv'.format(suffix)   
#     df = pd.read_csv(filename)
#     df_list.append(df)
# output = pd.concat(df_list)
# print(output)
# fname = r'C:\Users\yuki\Desktop\data_{}.csv'.format(date.today())
# output.to_csv(fname, encoding='utf-8', index=False)
########################################################

# clean data
df = web_spider.clean_data('data_2023-07-06')
print(df)
web_spider.update_sql(df, 'gz')


