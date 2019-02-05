# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from server import CarInfoFetcher
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    carInfoFetcher = CarInfoFetcher()
    resp = carInfoFetcher.get('http://eacodingtest.digital.energyaustralia.com.au/api/v1/cars')        
    
    if carInfoFetcher.status_code == 200:
        app.logger.info('Fetch Success! DataSize: %d' % (len(resp)))
        pass
    else:
        app.logger.error('Response:%s, ErrorCode:%d' % (resp, carInfoFetcher.status_code))
    
    return str(carInfoFetcher.status_code)
    
    #try:
    #    data = carInfoFetcher.get('http://eacodingtest.digital.energyaustralia.com.au/api/v1/cars')
    #    carInfoFetcher.printDataInOrder()
    #    return 'Hello'
    #except Exception as error:
    #    return error