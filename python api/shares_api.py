import http.client
import json

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6fe53e80bdmsh4a1843921687ec0p12c523jsnad1a15acd387",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

conn.request("GET", "/stock/v2/get-summary?symbol=SPCE&region=GB", headers=headers)

res = conn.getresponse()
data = res.read()

d = data.decode("utf-8")

e = json.loads(d)

print('$'+str(e['price']['regularMarketPrice']['raw']))