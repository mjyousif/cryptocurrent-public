import requests
from sorter import *

CMCKEY='*'

#Stuff to deal with multiple coins
class coinClass:
    def __init__(self, coinQuery, currency, jsonList,sortType):
        self.coinQuery=coinQuery
        self.currency=currency
        self.jsonList=jsonList
        self.sortType=sortType
        
class cryptoClass:
        
    def __init__(self, coinInfo, currency):
        #Will have access to : id,name, symbol, price, market_cap, percent_change_1h, percent_change_24h, percent_change_7d, currency
    
        self.id=str(coinInfo['id'])
        self.currency=currency
        #Name Check
        if(coinInfo['name']==None):
            self.name='N/A'
        else:
            self.name= coinInfo['name']
        
        #Symbol Check
        if(coinInfo['symbol']==None):
            self.symbol='N/A'
        else:
            self.symbol= coinInfo['symbol']
        
        #Price Check
        if(coinInfo['quote'][currency]['price']==None):
            self.price='N/A'
        else:    
            self.price=self.priceCommaPrecision(coinInfo['quote'][currency]['price'])
            
        #Market Cap Check
        if(coinInfo['quote'][currency]['market_cap']==None):
            self.market_cap='N/A'
        else:
            self.market_cap=self.priceCommaPrecision(coinInfo['quote'][currency]['market_cap'])
        #1h check
        if(coinInfo['quote'][currency]['percent_change_1h']==None):
            self.percent_change_1h='N/A'
        else:
            self.percent_change_1h=str(coinInfo['quote'][currency]['percent_change_1h'])
        
        #1d check
        if(coinInfo['quote'][currency]['percent_change_24h']==None):
            self.percent_change_24h='N/A'
        else:
            self.percent_change_24h=str(coinInfo['quote'][currency]['percent_change_24h'])
        
        #1w check
        if(coinInfo['quote'][currency]['percent_change_7d']==None):
            self.percent_change_7d='N/A'
        else:
            self.percent_change_7d=str(coinInfo['quote'][currency]['percent_change_7d'])
    #Make the price have commas and appropriate decimals
    def priceCommaPrecision(self, price):
        priceStr=str(price)
        priceStr=priceStr.split('.')
        if(price>=1.00):
            priceStr[1]=priceStr[1][0:2]
        else:
            priceStr[1]=priceStr[1][0:6]
        priceStr[0]="{:,}".format(int(priceStr[0]))
        priceStr='.'.join(priceStr)
        return priceStr
    
    
#this function is usually called whenever any query is passed
#it will return a list of each crypto with the price, market cap, etc, information in the given currency
def classifyQuery(query):
    acceptedCurrencies=["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD"]
    querySplit=query.split(" ")
    
    #Grab the sort type from end of query if it is there and remove. Do not otherwise
    sortTypes=["alpha","price","mktcap","1h","1d","7d"]
    if querySplit[-1].lower() in sortTypes:
        sortType=querySplit[-1]
        del querySplit[-1]
    else:
        sortType=""
    query=" ".join(querySplit)
    
    #default currency
    if not querySplit[-1].upper() in acceptedCurrencies:
        query+=" usd"
    currency=query[-3:].lower()
    
    #Getting the list of coins
    #formats the query properly (e.g. turns bitcoin cash to bitcoin-cash)
    query=query.replace(", ",",")
    query=query.lower()
    coinList=query[:-4].replace(" ","-")
    coinList=coinList.split(",")
    #getting the data of said coins
    cryptoList=[]
    i=0
    
    #Find the ID
    idList=[]
    listings=requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/map', headers={'X-CMC_PRO_API_KEY':CMCKEY})
    listings=listings.json()['data']
    #gets ID from map
    for coin in coinList:
        for x in (range(0,len(listings))):
            if (coin==listings[x]['name'].lower() or coin==listings[x]['symbol'].lower() or coin==listings[x]['slug'].lower()):
                idList.append(listings[x]['id'])
                break
    idListString=(','.join(str(x) for x in idList))
    #Get the specific information
    currency=currency.upper()
    coinInfo=requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest', params={'id':idListString, 'convert':currency},headers={'X-CMC_PRO_API_KEY':CMCKEY})
    coinInfoList=[]
    for coinID in idList:
        coinInfoList.append(coinInfo.json()['data'][str(coinID)])
   
    
    for i in range(len(coinList)):
        cryptoList.append(cryptoClass(coinInfoList[i],currency))
    cryptoList=valueSorter(cryptoList, sortType)
   
    return cryptoList
#------------------------------------------------------------------
#comma separated numbers that are entered as strings
#keeps precision of the numbers as shown in the coinmarketcap api in usd
def prettyANDprecise(strNum):
    numStrSplit=(strNum.split('.',1))
    numStrFormatLeft="{:,}".format(float(numStrSplit[0]))
    numStrFormatLeft=(numStrFormatLeft.split('.',1))
    if (len(numStrSplit)==1):
        pApOutput=numStrFormatLeft[0]
    else:
        pApOutput=(str(numStrFormatLeft[0])+'.'+numStrSplit[1])
    return pApOutput
    
