import pandas as pd
import requests

#Data Collection
url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory'
req = requests.get(url)
data_list = pd.read_html(req.text)
target_df = data_list[11] #Table one containing Country, Deaths per Million, Total Deaths, Total Cases
target_df2 = data_list[17] #Table containing Country and Vaccinated

#Data Cleaning 
target_df.columns = ['Col0', 'Country', 'Deaths per Million', 'Total Deaths', 'Total Cases']
target_df = target_df[['Country', 'Deaths per Million', 'Total Deaths', 'Total Cases']]

target_df2.columns = ['Col0', 'Country', 'Vaccinated', '% Vaccinated']
target_df2 = target_df2[['Country', 'Vaccinated']]

#Deleting extra Rows
target_df =target_df.drop([217])
last_idx = target_df.index[-1]
target_df = target_df.drop([last_idx])

#Removing inconsistent country names
target_df['Country'] = target_df['Country'].str.replace('\[.*\]','')
target_df2['Country'] = target_df2['Country'].str.replace('\[.*\]','')

#Converting string data types to int
target_df['Total Deaths'] = target_df['Total Deaths'].str.replace('—','0')
target_df['Deaths per Million'] = target_df['Deaths per Million'].str.replace('—','0')
target_df['Total Cases'] = pd.to_numeric(target_df['Total Cases'])
target_df['Deaths per Million'] = pd.to_numeric(target_df['Deaths per Million'])
target_df['Total Deaths'] = pd.to_numeric(target_df['Total Deaths'])

#Merging both t table data using Inner join
target_final_df = pd.merge(left=target_df2 , right=target_df , left_on='Country', right_on='Country')
target_final_df.shape

#Export Data in csv format
target_final_df.to_csv(r'covid19_database.csv')