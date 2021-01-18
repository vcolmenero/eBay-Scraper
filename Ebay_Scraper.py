import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'pokemon555'

def get_data(searchterm):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+cards+charizard&_sacat=0&LH_TitleDesc=0&_sop=12&_dcat=183454&Language=English&Character=Charizard&_ipg=200&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
            'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip()),
            'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)