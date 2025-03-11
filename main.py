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


# The code above only downloads the required csv file for the lab if the file doesn't exist already 
data = pd.read_csv(data_path)
print(f'Data successfuly read and stored into a pandas data frame \n {data.head(10)} ')
print(f'The shape of our data frame = {data.shape}')
print(f'This tells us that we have {data.shape[0]} rows and {data.shape[1]} columns ')
print(f'Data info \n{data.info}')
print(f'Data description \n{data.describe}')
print(f'Checking for missing values in the data {data.isnull().sum()}')
print (f'The columns of are data frame are as follows \n {data.columns}')
gasoline = data[['REF_DATE','GEO','Type of fuel','VALUE']].rename(columns={"REF_DATE":"DATE","Type of fuel":"TYPE"})
print(f'Filtered data \n {gasoline.head()}')
gasoline[['City','Province']]=gasoline['GEO'].str.split(',',n=1,expand=True)
print(gasoline.head())
gasoline['DATE']=pd.to_datetime(gasoline['DATE'],format='%b-%y')
# Converting the date column into a datetime object 
print(f'date column after converstion {gasoline['DATE']}')
gasoline['Month']=gasoline['DATE'].dt.month_name().str.slice(stop=3)
# extracts the month from the datetime object and converts it into a str e.g januray stop three slices januray
# into jan
gasoline['Year']=gasoline['DATE'].dt.year
print(f'Printingg the data set after date conversion \n {gasoline.head()}')
print(gasoline['VALUE'].describe())
print(f'Printing the unique values of locations from the data set insuring no duplicates are found \n {gasoline['GEO'].unique().tolist()}')
# the .unique() function selects all the unique values ensuring the duplicates are not selected 
print(f'\nPrinting all the categories from the types columns \n {gasoline['TYPE'].unique().tolist()}')
# Now we will start filtering the data 
calgary_albarta = gasoline[gasoline['GEO']=='Calgary, Alberta']
# Creates a new dataframe and stores it into our varable having rows only equal to the string provided 
print(calgary_albarta)
# calgary_albarta = gasoline['GEO']=='Calgary, Alberta' will return true for the row where our string is present so it is a boolean series 
