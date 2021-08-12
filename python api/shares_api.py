import http.client

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6fe53e80bdmsh4a1843921687ec0p12c523jsnad1a15acd387",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

conn.request("GET", "/auto-complete?q=SPCE&region=GB", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))