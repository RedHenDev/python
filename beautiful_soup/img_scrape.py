import requests
from bs4 import BeautifulSoup
import os

url = "https://ccc.tela.org.uk/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]

for i, url in enumerate(urls):
    print('found another...')
    response = requests.get(url)
    with open(f'img{i}.jpg', 'wb') as f:
        f.write(response.content)


