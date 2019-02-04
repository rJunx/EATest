# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import json
import pandas as pd

class App:
    def __init__(self):
        self.df = pd.DataFrame({'make':[], 'model':[], 'name':[]})
        
    def get(self, url):
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            resp = e.read()
            self.status_code = e.code
            raise Exception(resp)
        except urllib2.URLError, e:
            resp = e.read()
            self.status_code = e.code
            raise Exception(resp)
        else:
            self.status_code = response.code
            resp = json.loads(response.read())
            resp = self.toDataFrame(resp)
            
        return resp
    
    def getValueByKey(self, item, key, default='Unknown'):
        if item.has_key(key):
            if item[key]=='':
                return default
            else:
                return item[key]
        else:
            return default
    
    def toDataFrame(self, dList):
        #make model name        
        for item in dList:
            name = self.getValueByKey(item, 'name', '')
            cars = self.getValueByKey(item, 'cars', [])
            
            for car in cars:
                self.df = self.df.append({'make': self.getValueByKey(car, 'make'), 
                                'model': self.getValueByKey(car, 'model', ''), 
                                'name':name}, ignore_index=True)

        return self.df
    
    def printDataInOrder(self):
        df = self.df.sort_values(by=['make', 'model', 'name'])
        for _, row in df.iterrows():
            print row['make']
            print " "*5 + row['model']
            print " "*10 + row['name']


if __name__ == "__main__":
    myApp = App();
    
    try:
        myApp.get('http://eacodingtest.digital.energyaustralia.com.au/api/v1/cars')
        myApp.printDataInOrder()
    except Exception as error:
        print repr(error)
