# -*- coding: utf-8 -*-

import urllib2
import json
import pandas as pd

class CarInfoFetcher:
    '''  
    The module is to fetch car data from the API and store the data into a memory database (Pandas)
    '''
    
    def __init__(self):
        self.__df = pd.DataFrame({'make':[], 'model':[], 'name':[]})
        self.statusCode = 200
        
    
    def get(self, url):
        '''
        Fetch the data from a specific URL
        :return: the raw message from backend
        '''
        
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            resp = e.read()
            self.statusCode = e.code
        except urllib2.URLError, e:
            resp = e.read()
            self.statusCode = e.code
        else:
            self.statusCode = response.code
            resp = response.read()
            self.__toDataFrame(json.loads(resp))
            
        return resp
    
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


    #Private method to 
    def __getValueByKey(self, item, key, default='Unknown'):
        if item.has_key(key):
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