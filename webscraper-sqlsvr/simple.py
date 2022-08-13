import pyodbc
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

url = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky'

def soup(url:str) -> BeautifulSoup:
  return BeautifulSoup(requests.get(url).content,'lxml')

# data processing
def soup_to_df(soup) -> pd.DataFrame:
    prod_content = soup.find_all('div', class_="product-card__content")
    prod_data = soup.find_all('div', class_="product-card__data")
    # Should not processing if both tags not containing same number of items!
    if len(prod_content) != len(prod_data):
        raise Exception('The webpage contents is missing something')
    
    df = pd.DataFrame(columns=['name', 'volumn(cl)', 'alcohol', 'price(£)', 'price/l'])
    for i in range(len(prod_content)):
        templist = [
            # product name
            prod_content[i].find('p',class_="product-card__name").text.strip(),
            # price all in '£'
            float(prod_data[i].find('p',class_="product-card__price").text.strip().strip('£')),
            # unit price
            float(re.sub('[^\d\.]','', 
                prod_data[i].find('p',class_="product-card__unit-price").text.strip()))
            ]
        # volumn and alcohol format like '70cl / 46.3%'
        cardmeta = prod_content[i].find('p',class_="product-card__meta").text.strip().split('/')
        templist.insert(1,
            float(cardmeta[1].strip().strip('%')))
        templist.insert(1,
            int(cardmeta[0].strip().strip('cl')))
        tempdf = pd.DataFrame(
            [templist],
            columns=['name', 'volumn(cl)', 'alcohol(%)', 'price(£)', 'unitprice'])
        df = pd.concat([df,tempdf],ignore_index=True)

    return df

def df_to_sqlsvr(df:pd.DataFrame) -> None:
    #sql server settings
    sqlserver = 'localhost'
    database = 'ETL'
    username = 'etl'
    password = 'mypass#688'
    connection_string = 'DRIVER={ODBC Driver 18 for SQL Server};TrustServerCertificate=YES;SERVER='+sqlserver+';DATABASE='+database+';UID='+username+';PWD='+ password
    SQL = "INSERT INTO [dbo].[Products]([Item],[Price],[Volumn],[UnitPrice],[Alcohol]) VALUES(?,?,?,?,?)"

    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        print('inserting data to sql server...')
        for _, row in df.iterrows():
            cursor.execute(SQL, row['name'], row['volumn(cl)'], row['alcohol(%)'], row['price(£)'], row['unitprice'])
        cnxn.commit()
        print('insert finished!')

    except Exception as e:
        print("Extract/sql server Error: ",e)

    finally:
        cursor.close()
        cnxn.close()

if __name__ == "__main__":
    soup = soup(url)

    # get how many pages
    pages = int(soup.find('nav', class_ = "paging js-paging").attrs['data-totalpages'])

    #get content from the first(main) page
    df = soup_to_df(soup)

    #get data from the following pages
    for page in range(pages):
        print(f'scraping {page} out of {pages}...')
        soup(url+'?pg='+str(page))
        df = pd.concat([df,soup_to_df(soup)],ignore_index=True)

    print(f'finished web scraping with {df.size} items')
    df.to_csv('wisky.csv',index=False)
    df_to_sqlsvr(df)