# -*- coding: utf-8 -*-

import requests
import pandas as pd
from requests.exceptions import HTTPError, ConnectionError
from json.decoder import JSONDecodeError

class CarInfoFetcher:
    '''  
    The module is to fetch car data from the API and store the data into a memory database (Pandas)
    '''
    
    def __init__(self):
        self.__df = pd.DataFrame({'make':[], 'model':[], 'name':[]})
        self.statusCode = -1
        
    def get(self, url):
        '''
        Fetch the data from a specific URL
        :return: the raw message from backend
        '''
        try:
            response = requests.get(url, timeout=1)
            self.statusCode = response.status_code
            self.__toDataFrame(response.json())
            return response.text
        except HTTPError as e:
            self.statusCode = response.status_code
            return response.text
        except ConnectionError as e:
            self.statusCode = -1
            return 'ConnectionError'
        except JSONDecodeError as e:
            return response.text
    
    def getDataFrame(self):
        '''
        Get the dataframe generated from the successful reponse
        :return: DataFrame (Pandas)
        '''
        return self.__df
    
    def printDataInOrder(self, spaceSymbol='', breakLineSymbol='\n'):
        df = self.__df.sort_values(by=['make', 'model', 'name'])
        ret = ''
        for _, row in df.iterrows():
            ret = ret + row['make'] + breakLineSymbol
            ret = ret + spaceSymbol*5 + row['model'] + breakLineSymbol
            ret = ret +  spaceSymbol*10 + row['name'] + breakLineSymbol
        return ret

    def __getValueByKey(self, item, key, default='Unknown'):
        if key in item:
            if item[key]=='':
                return default
            else:
                return item[key]
        else:
            return default
    
    def __toDataFrame(self, dList):
        #make model name        
        for item in dList:
            name = self.__getValueByKey(item, 'name')
            cars = self.__getValueByKey(item, 'cars', [])
            
            for car in cars:
                self.__df = self.__df.append({'make': self.__getValueByKey(car, 'make'), 
                                'model': self.__getValueByKey(car, 'model'), 
                                'name':name}, ignore_index=True)