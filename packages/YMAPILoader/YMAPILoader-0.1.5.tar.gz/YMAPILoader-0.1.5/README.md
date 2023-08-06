# About the library
A library to download data from Yandex Metrica API.

### Installation
```
pip install YMAPILoader
```

### Code example
How to download data from Yandex Metrica API with this lib:

```Python
from YMAPILoader import YMAPILoader

TOKEN = "YOUR API TOKEN"
YM_TRACKER_ID = "123456"
START_DATE = '2022-05-01'
END_DATE = '2022-06-30'
METRICS = 'ym:s:visits'
DIMENSIONS = 'ym:s:referer'

data_params = {
        "metrics": METRICS,
        "dimensions": DIMENSIONS,
        "ids": YM_TRACKER_ID,
        "date1": START_DATE,
        "date2": END_DATE,
        "filters": "ym:s:isRobot=='No'",
        "accuracy": '1',
        }
data_loader = YMAPILoader(TOKEN, data_params)
data_loader.load_all_data()
data = data_loader.data
```
It downloads all available data and returns it as a Pandas DataFrame, if no error occures. 
Please, do not use parameters "limit" and "offset" in data_params.
