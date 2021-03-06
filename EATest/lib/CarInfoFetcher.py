# -*- coding: utf-8 -*-

import requests
import urllib3
import json
import pandas as pd
from json.decoder import JSONDecodeError
from cachecontrol import CacheControlAdapter
from cachecontrol.heuristics import ExpiresAfter

class CarInfoFetcher:
    '''  
    The module is to fetch car data from the API and store the data into a memory database (Pandas)
    '''
   
    def __init__(self, url, max_retries, expires_after_sec):
        self.hasError = False
        self.fromCache = False
        self.url = url
        self.cacheEnabled = expires_after_sec > 0
        self.session = requests.Session()
        retryPolicy = urllib3.util.Retry(max_retries, status_forcelist=[400])
        if self.cacheEnabled:
            self.session.mount(url, CacheControlAdapter(max_retries=retryPolicy, heuristic=ExpiresAfter(seconds=expires_after_sec)))
        else:
            self.session.mount(url, requests.adapters.HTTPAdapter(max_retries=retryPolicy))
            
    def requestData(self):
        '''
        Request car data from the API 
        :return: message string
        '''
        try:
            response = self.session.get(self.url)
            self.hasError = response.status_code != 200
            self.fromCache = False if(not self.cacheEnabled) else response.from_cache

            if not self.hasError:
                try:
                    return response.json()
                except JSONDecodeError:
                    return []
            
            return response.text
        except urllib3.exceptions.MaxRetryError as e:
            self.hasError = True
            return str(e)
        except Exception as e:
            self.hasError = True
            return e
    
    def printDataInOrder(self, df, spaceSymbol='', breakLineSymbol='\n'):
        '''
        Format output for DataFrame
        :return: DataFrame (Pandas)
        '''
        df = df.sort_values(by=['make', 'model', 'name'])
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
    
    def toDataFrame(self, dList):
        '''
        Transform json data to DataFrame
        :return: DataFrame (Pandas)
        '''
        #make model name
        df = pd.DataFrame({'make':[], 'model':[], 'name':[]})

        for item in dList:
            name = self.__getValueByKey(item, 'name')
            cars = self.__getValueByKey(item, 'cars', [])
            
            for car in cars:
                df = df.append({'make': self.__getValueByKey(car, 'make'), 
                                'model': self.__getValueByKey(car, 'model'), 
                                'name':name}, ignore_index=True)

        return df