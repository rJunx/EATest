# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from CarInfoFetcher import CarInfoFetcher
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def home():
    carInfoFetcher = CarInfoFetcher()
    attempTime = 0      
    hasError = True
    resp = ''
    
    #Auto attemp to fetch data with any conection error 
    while (attempTime <= app.config['FAIL_RETRY_TIMES'] and hasError):
        resp = carInfoFetcher.get(app.config['API'])
        hasError = carInfoFetcher.statusCode != 200
        attempTime = attempTime + 1
        if hasError:
            app.logger.error('Response:%s, ErrorCode:%d, Retry:%d'% (resp, carInfoFetcher.statusCode,attempTime))
    
    if hasError:
        app.logger.error('Response:%s, ErrorCode:%d' % (resp, carInfoFetcher.statusCode))
        return resp
    else:
        app.logger.info('Fetch Success! DataSize: %d' % (len(resp)))
        df = carInfoFetcher.getDataFrame()
        if app.config['SHOW_IN_TABLE']:
            return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
        else:
            return carInfoFetcher.printDataInOrder('&nbsp;', '<br>')
    