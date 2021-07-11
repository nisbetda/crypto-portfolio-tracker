from cmc_api_key import api_key
from portfolio import symbols, symbol_list, BTC, ETH, XLM, XMR, ADA, ALGO
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import pandas as pd
import numpy as np
import plotly.express as px
import plotly
from datetime import date
#google api: from pytrends.request import TrendReq


#Call the API, the variable data is "returned"
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':symbols,
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}
session = Session()
session.headers.update(headers)
try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  pprint.pprint(data) #<--------- all the DATA
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

#=========================================================================================================================================================
#Find Portfolio USD Value
#USE A FUNCTION OR SOMETHING!!!!!!!!!!
#get_price function
def get_price(price_symbol):
  for d in data:
    price = data['data'][price_symbol]['quote']['USD']['price']
  return price

#Calculations To Find Portfolio Value
bitcoin_price =  get_price('BTC')
ethereum_price =  get_price('ETH')
lumen_price =  get_price('XLM')
monero_price =  get_price('XMR')
algorand_price = get_price('ALGO')
cardano_price = get_price('ADA')
bitcoin_value = BTC * bitcoin_price 
ethereum_value = ETH * ethereum_price 
lumen_value = XLM * lumen_price 
monero_value = XMR * monero_price 
cardano_value = ADA * cardano_price 
algorand_value = ALGO * algorand_price
portfolio_value = bitcoin_value + ethereum_value + lumen_value + monero_value + cardano_value + algorand_value
pprint.pprint('=========================================================================================================================================================')

#Calculate and Print Percentages
bitcoin_percent = (100*bitcoin_value/portfolio_value)
ethereum_percent = (100*ethereum_value/portfolio_value) 
monero_percent = (100*monero_value/portfolio_value) 
lumen_percent = (100*lumen_value/portfolio_value) 
cardano_percent = (100*cardano_value/portfolio_value) 
algorand_percent = (100*algorand_value/portfolio_value)


#Calculations To Find BTC Value of each coin
bitcoin_BTC_value = BTC 
ethereum_BTC_value = ethereum_value / bitcoin_price
lumen_BTC_value = lumen_value / bitcoin_price
monero_BTC_value = monero_value / bitcoin_price
cardano_BTC_value = cardano_value / bitcoin_price
algorand_BTC_value = algorand_value / bitcoin_price
portfolio_BTC_value = bitcoin_BTC_value + ethereum_BTC_value + monero_BTC_value + lumen_BTC_value + cardano_BTC_value + algorand_BTC_value

#Print Percentages 
pprint.pprint('Percentages')
pprint.pprint('     BTC: '+ str(round(bitcoin_percent)) + '%')
pprint.pprint('     ETH: '+ str(round(ethereum_percent)) + '%')
pprint.pprint('     XMR: '+ str(round(monero_percent)) + '%')
pprint.pprint('     XLM: '+ str(round(lumen_percent)) + '%')
pprint.pprint('     ADA: '+ str(round(cardano_percent)) + '%')
pprint.pprint('     ALGO: '+ str(round(algorand_percent)) + '%')
pprint.pprint('=========================================================================================================================================================')

#print Value in BTC
pprint.pprint('Value of Portfolio (BTC): '+ str(round(portfolio_BTC_value, 8)))
pprint.pprint('     BTC: '+ str(round(bitcoin_BTC_value, 3)))
pprint.pprint('     ETH: '+ str(round(ethereum_BTC_value, 3)))
pprint.pprint('     XMR: '+ str(round(monero_BTC_value, 3)))
pprint.pprint('     XLM: '+ str(round(lumen_BTC_value, 3)))
pprint.pprint('     ADA: '+ str(round(cardano_BTC_value, 3)))
pprint.pprint('     ALGO: '+ str(round(algorand_BTC_value, 3)))

pprint.pprint('=========================================================================================================================================================')
#print Values in USD

pprint.pprint('Value of Portfolio (USD): ' + str(round(portfolio_value)))
pprint.pprint('     BTC: '+ str(round(bitcoin_BTC_value*bitcoin_price)))
pprint.pprint('     ETH: '+ str(round(ethereum_BTC_value*bitcoin_price)))
pprint.pprint('     XMR: '+ str(round(monero_BTC_value*bitcoin_price)))
pprint.pprint('     XLM: '+ str(round(lumen_BTC_value*bitcoin_price)))
pprint.pprint('     ADA: '+ str(round(cardano_BTC_value*bitcoin_price)))
pprint.pprint('     ALGO: '+ str(round(algorand_BTC_value*bitcoin_price)))
pprint.pprint('=========================================================================================================================================================')


#=========================================================================================================================================================
#Starburst Szn
#step 1: create dataFrame
data_frame = {
        'Crypto':[portfolio_BTC_value,portfolio_BTC_value,portfolio_BTC_value,portfolio_BTC_value,portfolio_BTC_value,portfolio_BTC_value],
        'Name':['BTC', 'ETH', 'XLM', 'XMR', 'ADA', 'ALGO'],
        'Algorithm':['POW', 'POS', 'SCP', 'POW', 'POS', 'PPOS'],
        'Quantity':[BTC, ETH, XLM, XMR, ADA, ALGO],
        'USD Price':[bitcoin_price, ethereum_price, lumen_price, monero_price, cardano_price, algorand_price],
        'BTC Value':[bitcoin_BTC_value, ethereum_BTC_value, lumen_BTC_value, monero_BTC_value, cardano_BTC_value, algorand_BTC_value],
        'USD Value':[bitcoin_value, ethereum_value, lumen_value, monero_value, cardano_value, algorand_value],
        'Percent':[round(bitcoin_percent), round(ethereum_percent), round(lumen_percent), round(monero_percent), round(cardano_percent,2), round(algorand_percent,2)]}

df = pd.DataFrame(data_frame)
print(df)

#step 2: export to excel
today = date.today()
print("Today's date:", today)
filename = 'frame_the_data' + str(today) + '.xlsx'
df.to_excel(filename)




df = pd.read_excel(filename, engine='openpyxl',)







#This sunburst isn't organized well!!!!!!!!!!!!!!!!!<------------------------
#can categorize based on POS,POW,PPOS
#or maybe percent_change_90d, cmc_rank, volume_24h, max_supply

#Percent Change Analysis w/ Sunburst
#Step 1: Declare And Assign 6 Percent Change Variables for each Asset
def get_percent_change(quote_symbol):
  percent_change_list = []
  num_of_symbols = 0
  for s in symbol_list:
      num_of_symbols += 1
      percent_change_1h = data['data'][s]['quote']['USD']['percent_change_1h']
      percent_change_24h = data['data'][s]['quote']['USD']['percent_change_24h']
      percent_change_7d = data['data'][s]['quote']['USD']['percent_change_7d']
      percent_change_30d = data['data'][s]['quote']['USD']['percent_change_30d']
      percent_change_60d = data['data'][s]['quote']['USD']['percent_change_60d']
      percent_change_90d = data['data'][s]['quote']['USD']['percent_change_90d']

      percent_change_list.append(percent_change_1h)
      percent_change_list.append(percent_change_24h)
      percent_change_list.append(percent_change_7d)
      percent_change_list.append(percent_change_30d)
      percent_change_list.append(percent_change_60d)
      percent_change_list.append(percent_change_90d)

  df_percent = pd.DataFrame(percent_change_list)

  return df_percent, num_of_symbols

#Step 2: Create Data Frame for variables
percents, num_of_symbols =  get_percent_change(symbol_list)
#change dimensions
new_percents = percents.values.copy()
#converted to a numpy array, why? idk.
new_percents.resize((len(symbol_list)), 6) #find a way to find length of list of symbols
pd.DataFrame(new_percents.T)
# convert array into a dataframe
df_from_np = pd.DataFrame(new_percents.T)
# save to xlsx file
df_from_np.to_excel('new_percents.xlsx', index = ['BTC', 'ETH', 'XLM', 'XMR', 'ALGO', 'ADA'], header = ['percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 'percent_change_60d', 'percent_change_90d'])

#INDEX NEEDS TO BE AUTOMATIC (for more symbols 10k+)!!!! <----------------------------------------------------------------------

#pprint.pprint(new_percents)

#Step 3: Make another Sunburst with percents
#read the data from frame_the_data file  and the new_percents file
df_portfolio = pd.read_excel('frame_the_data.xlsx', engine='openpyxl',)
df_percent = pd.read_excel('new_percents.xlsx', engine='openpyxl',)

Name = df_portfolio['Name']
Quantity = df_portfolio['Quantity']
USD_Price = df_portfolio['USD Price']
USD_Value = df_portfolio['USD Value']
BTC_Value = df_portfolio['BTC Value']

percent_change_1h = df_percent['percent_change_1h']
percent_change_24h = df_percent['percent_change_24h']
percent_change_7d = df_percent['percent_change_7d']
percent_change_30d = df_percent['percent_change_30d']
percent_change_60d = df_percent['percent_change_60d']
percent_change_90d = df_percent['percent_change_90d']

percent_name_list = ['percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 'percent_change_60d', 'percent_change_90d']
percent_value_list = [percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d]

#find the number of positive percentage changes for each symbol
#split dataframe by row
df_percent_1 = df_percent.iloc[0,:]
df_percent_2 = df_percent.iloc[1,:]
df_percent_3 = df_percent.iloc[2,:]
df_percent_4 = df_percent.iloc[3,:]
df_percent_5 = df_percent.iloc[4,:]
df_percent_6 = df_percent.iloc[5,:]

hour_1 = df_percent_1.iloc[[0,1]]
hour_24 = df_percent_1.iloc[[0,2]]
day_7 = df_percent_1.iloc[[0,3]]
day_30 = df_percent_1.iloc[[0,4]]
day_60 = df_percent_1.iloc[[0,5]]
day_90 = df_percent_1.iloc[[0,6]]
#Why Are These Values Not Regular Ints?????? <----------
#print(percent_change_1h.take[[0,0]])
 
#how to get the number value?????
#reorganize dataframe with symbol as the index
#get rid of index value
#finish sunburst
#def get_percent_change(quote_symbol):
  #for s in symbol_list:
#the visualization party pt. 2
fig = px.sunburst(
                 path = [Name],
                 #color = percent_value_list,
                 color_continuous_scale = ['red', 'green'],
                 title = 'Crypto Percents'
                 )
#plotly.offline.plot(fig, filename = 'Crypto_Percent_Sunburst.html')
#Step 4: Profit??????
#=========================================================================================================================================================


#more colors

#Use twitter API to track Founders

print('bye')
#print("A MOLNAR & NISBETT CONSULTING PROGRAM")
