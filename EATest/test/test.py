from .lib.CarInfoFetcher import CarInfoFetcher

carInfoFetcher = CarInfoFetcher()
resp = carInfoFetcher.get(app.config['API'], app.config['FAIL_RETRY_TIMES'])

print(resp)