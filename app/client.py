import requests
import pandas as pd 
from pprint import pprint
df = pd.read_csv("/home/thays/Documents/employee-attrition/employee-attrition/data/01_raw/employee-attrition.csv")
df = df.sample(1)

url = 'http://127.0.0.1:12345/prediction'
myobj = df.to_dict('records')[0]
pprint(myobj)

x = requests.post(url, json = myobj)
 
print(x.text)
