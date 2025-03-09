import pandas as pd 
import plotly.express as px
import datetime
import requests
import os 
import json
data_folder = 'data'
os.makedirs(data_folder,exist_ok=True)
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/18100001.csv'
data_path = os.path.join(data_folder,'gasoline.csv')
if os.path.exists(data_path):
    print(f'File saved at {data_path}')
else:
    response = requests.get(url)
    with open(data_path,'wb') as file:
        file.write(response.content)
    print(f'File downloaded succesfully and saved at {data_path}')

