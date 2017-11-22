import pymongo
import pandas as pd
import os

client = pymongo.MongoClient()
db = client['mck_studies']
collection = db['vip_regional']

data_path = 'C:/Users/Ruofei Shen/Desktop/mck_studies/唯品会组织转型/样本数据/第二次样本数据/orderlist1.csv'
pwd = os.getcwd()
os.chdir(os.path.dirname(data_path))
data = pd.read_csv(os.path.basename(data_path), encoding='gbk')
os.chdir(pwd)

data2 = data[['user_id', 'goods_amount', 'brand_store_level_new', 'new_category_1st_name','p_brand_sn']]
data2.loc[:, 'user_id'] = data2['user_id'].astype(float)
data2.loc[:, 'goods_amount'] = data2['goods_amount'].astype(float)
data_dict = dict(data2)
data_dict = {key: list(value) for key, value in data_dict.items()}

collection.insert_many(data_dict)

