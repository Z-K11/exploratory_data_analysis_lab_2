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
gasoline_2000 = gasoline[gasoline['Year']==2000]
print(f'\nFiltered rows using year \n {gasoline_2000}')
# Let's perform multiple filteration using mutliple condition 
multiple_condition = gasoline[(gasoline['GEO']=='Toronto, Ontario')|(gasoline['GEO']=='Edmonton, Alberta')]
print(f'Printing the data set after performing filteration using mutliple conditions \n {multiple_condition}')
# We can also use isin method to select multiple conditions in an easier way using lists 
Cities = ['Calgary','Toronto','Edmonton']
isin_filtered = gasoline[gasoline['City'].isin(Cities)]
print(f'Filetering data using multiple conditions using the is in method \n {isin_filtered}')
print('\nThis method is readable and more cleaner as you can tell')
print('Selecting the data that shows the price of ousehold heating fuel in Vancouver in 1990')
ans = gasoline[(gasoline['TYPE']=='Household heating fuel')&(gasoline['City']=='Vancouver')&(gasoline['Year']==1990)]
years=[2021,1979,1990]
ans = gasoline[(gasoline['TYPE']=='Household heating fuel')&(gasoline['City']=='Vancouver')&(gasoline['Year'].isin(years))]
ans = gasoline[(gasoline['TYPE']=='Household heating fuel')&(gasoline['City']=='Vancouver')&(gasoline['Year'].isin(years))]
print(f'ans = {ans}')
ans = gasoline[(gasoline['TYPE']=='Household heating fuel')&(gasoline['City']=='Vancouver')]
print('Verifying if our approach is correct')
print(ans['Year'].unique())
# our filtering works properly 
geo = gasoline.groupby('GEO')
print(geo.ngroups)
'''Most commonly, we use groupby() to split the data into groups,this will apply some function to each of the groups 
(e.g. mean, median, min, max, count), then combine the results into a data structure.
For example, let's select the 'VALUE' column and calculate the mean of the gasoline prices per year.
First, we specify the 'Year" column, following by the 'VALUE' column, and the mean() function.'''
group_year=gasoline.groupby('Year')['VALUE'].mean()
print(f'Mean of values grouped per year = {group_year} no. of groups = {gasoline.groupby('Year').ngroups}')
print('The groupby method groups unique values')
exercise = gasoline.groupby('Month')['VALUE'].max()
# grouping by month with max price value 
exercise2 = gasoline.groupby(['Year','City'])['VALUE'].median().reset_index(name='VALUE').round(2)
print(exercise2)
# let's plot the price of gasoline in all cities during 1979-2021
price_bycity = gasoline.groupby(['Year','GEO'])['VALUE'].mean().reset_index(name='VALUE').round(2)
print(f'Price of gaslone classified by city {price_bycity}')
fig = px.line(price_bycity,x='Year',y='VALUE',color='GEO',color_discrete_sequence=px.colors.qualitative.Light24)
fig.update_layout(title="Gasoline Price Trend per City",
    xaxis_title="Year",
    yaxis_title="Annual Average Price, Cents per Litre")
fig.update_traces(mode='markers+lines')
fig.show()

one_year=gasoline[gasoline['Year']==2021]
print(f'Average values of gasoline through years \n {one_year.head()}')
month_trend= gasoline[(gasoline['Year']==2021)&(gasoline['GEO']=='Toronto, Ontario')]
group_month = month_trend.groupby(['Month'])['VALUE'].mean().reset_index(name='Average prices').sort_values(by='Average prices')
print(f'Average price of gas in tornonto for year 2021 = {group_month}')
fig =px.line(group_month,x='Month',y='Average prices')
fig.update_traces(mode='markers+lines')
fig.update_layout(title="Toronto Average Monthly Gasoline Price in 2021",
    xaxis_title="Month",
    yaxis_title="Monthly Price, Cents per Litre")
fig.show()
average = gasoline.groupby(['Year','TYPE'])['VALUE'].mean().reset_index().round(2)
fig = px.bar(average,x='TYPE',y='VALUE',animation_frame='Year')
fig.update_layout(title='Average anual gas prices',xaxis_title='Year',yaxis_title='Price')
fig.show()
# let's save the data of year 2021 in a separate variable 
one_year = gasoline[gasoline['Year']==2021]
print(f'Data Of year 2021 = \n{one_year}')
geo_data= one_year.groupby(['Province'])['VALUE'].mean().reset_index(name='Average gasoline price').round(2)
province_id={
    ' Newfoundland and Labrador' :5,
    ' Prince Edward Island':8,
    ' Nova Scotia':2,
    ' New Brunswick':7,
    ' Quebec':1,
    ' Ontario':11,
    ' Ontario part, Ontario/Quebec':12,
    ' Manitoba':10,
    ' Saskatchewan':3,
    ' Alberta':4,
    ' British Columbia':6,
    ' Yukon':9,
    ' Northwest Territories':13}
geo_data['ProvinceID']=geo_data['Province'].map(province_id)
print(geo_data)
geo = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/canada_provinces.geojson")
mp = json.loads(geo.text)
'''geo_data = "geo_data"
os.makedirs(geo_data,exist_ok=True)
geo_data_destination = os.path.join(geo_data,"data.geoJson")
url ="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/canada_provinces.geojson"
response = requests.get(url)
if os.path.exists(geo_data_destination):
    print(f'Data already exists at {geo_data_destination}')
else :
    with open(geo_data_destination,"wb") as file:
        file.write(response.content)
    print(f"file succesfully saved at path = {geo_data_destination}")
with open (geo_data_destination,"r",encoding="utf-8") as file:
    mp = json.loads(file.read())'''
fig = px.choropleth(geo_data,
                    locations="ProvinceID",
                    geojson=mp,
                    featureidkey="properties.cartodb_id",
                    color="Average gasoline price",
                    color_continuous_scale=px.colors.diverging.Tropic,
                    scope="north america",
                    title='<b>Averagr Gasoline Price</b>',
                    hover_name='Province',
                    hover_data={'Average gasoline price' : True,
                                'ProvinceID' : False},
                    locationmode='geojson-id',)
fig.update_layout(showlegend=True,
                  legend_title_text='<b>Average Gasoline Price</b>',
                  font={"size":16,"color":"#808080","family":"calibri"},
                  margin={"r":0,"t":40,"l":0,"b":0},
                  legend=dict(orientation='v'),
                  geo=dict(bgcolor='rgba(0,0,0,0)',lakecolor='#e0fffe'))
fig.update_geos(showcountries=False, showcoastlines=False,
                showland=False, fitbounds="locations",
                subunitcolor='white')
fig.show()