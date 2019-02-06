# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from lib.CarInfoFetcher import CarInfoFetcher
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')
carInfoFetcher = CarInfoFetcher(app.config['API'], app.config['FAIL_RETRY_TIMES'], app.config['EXPIRES_AFTER_SEC'])

@app.route("/")
def home():
    '''
    The simple homepage for showing the API response
    :return: html string
    '''
    resp = carInfoFetcher.requestData()
    
    if carInfoFetcher.hasError:
        app.logger.error(resp)
        return 'Oops! Fetching data failed......'
    else:
        app.logger.info('Fetch Success! DataSize: %d FromCache:%s' % (len(resp), carInfoFetcher.fromCache))
        df = carInfoFetcher.toDataFrame(resp)
        if app.config['SHOW_IN_TABLE']:
            return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
        else:
            return carInfoFetcher.printDataInOrder(df, '&nbsp;', '<br>')
    
@app.route("/ping_test")
def pingTest():
    return 'Benchmark Testing'