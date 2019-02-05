# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import json
import pandas as pd

class CarInfoFetcher:
    def __init__(self):
        self.__df = pd.DataFrame({'make':[], 'model':[], 'name':[]})
        
    def get(self, url):
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            resp = e.read()
            self.status_code = e.code
        except urllib2.URLError, e:
            resp = e.read()
            self.status_code = e.code
        else:
            self.status_code = response.code
            resp = json.loads(response.read())
            self.__toDataFrame(resp)
            
        return resp
        
    def printDataInOrder(self):
        df = self.__df.sort_values(by=['make', 'model', 'name'])
        for _, row in df.iterrows():
            print row['make']
            print " "*5 + row['model']
            print " "*10 + row['name']
            
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


#if __name__ == "__main__":
#    myApp = App();
    
#    try:
#        data = myApp.get('http://eacodingtest.digital.energyaustralia.com.au/api/v1/cars')
#        myApp.printDataInOrder()
#    except Exception as error:
#        print error
