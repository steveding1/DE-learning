import pandas as pd
from os.path import exists
import time 
import pytz
from datetime import datetime

def downld_weather():
    weath_url = 'https://forecast.weather.gov/MapClick.php?textField1=40.78&textField2=-73.97#.YtWW3HaZNhE'
    csvfname = '/home/sding/airflow/csvfiles/weath.csv'

    weath_df = pd.read_html(weath_url)[0].set_index(0).transpose()
    weath_df['Humidity'] = weath_df['Humidity'].str.extract('(\d+)').astype(int)
    weath_df['Barometer'] = weath_df['Barometer'].str.findall('(\d+)').str[1].astype(int)
    weath_df['Dewpoint'] = weath_df['Dewpoint'].str.findall('(\d+)').str[1].astype(int)
    weath_df['Visibility'] = weath_df['Visibility'].str.findall('(\d+)').str[1].astype(int)
    weath_df['Heat Index'] = weath_df['Heat Index'].str.findall('(\d+)').str[1].astype(int)
    weath_df['Last update'] = weath_df['Last update'].str.replace(' EDT','')+str(datetime.now().year)
    weath_df['Last update'] = pd.to_datetime(weath_df['Last update'], format='%d %b %I:%M %p%Y')
    if exists(csvfname):
        pd.read_csv(csvfname,parse_dates=[-1],infer_datetime_format='Y-m-D H:M:S')\
            .append(weath_df).drop_duplicates(subset=['Last update'], keep='last').to_csv(csvfname,index=False)
    else:
        weath_df.to_csv(csvfname,index=False)

def downld_electr():
    nydate = datetime.now(pytz.timezone("America/New_York")).strftime("%Y%m%d")
    elect_url = 'http://mis.nyiso.com/public/csv/pal/{0}pal.csv'.format(nydate)
    csvfname = '/home/sding/airflow/csvfiles/electricity.csv'
    elect_df = pd.read_csv(elect_url,parse_dates=[0],infer_datetime_format='Y-m-D H:M:S')
    elect_df = elect_df[elect_df['Name']=='N.Y.C.'][['Time Stamp','Load']].dropna(subset=['Load'])
    elect_df
    if exists(csvfname):
        pd.read_csv(csvfname,header=0,parse_dates=[0],infer_datetime_format='Y-m-D H:M:S')\
            .append(elect_df).drop_duplicates(subset=['Time Stamp'], keep='last').to_csv(csvfname,index=False)
    else:
        elect_df.to_csv(csvfname,index=False)
