from  bs4 import BeautifulSoup
import requests
import props_database
import re
from pony.orm import db_session

class DaftRss(object):
    '''
    Have API, is private.
    Conclusion: Fuck them
    '''
    @db_session
    def retrieve(self, rss, sqlite_conn):
        
        data = requests.get(rss)
        soup = BeautifulSoup(data.content, "lxml-xml")
        houses = []
        for house in soup.find_all('item'):
            g = re.match(r'([0-9,]+)\s+(\w+)', house.price.text)
            pr = float(g.group(1).replace(',',''))
            if g.group == 'weekly':
                pr = pr * 4
            img = ''
            soup2 = BeautifulSoup(house.description.text, 'lxml')
            if soup2.img:
                img = soup2.img.attrs['src']
            h = props_database.Property(
                title=house.title.text,
                description=house.description.text,
                price=pr,
                price_string=house.price.text,
                main_photo=img,
                address=house.address.text,
                position_longitude=float(house.long.text),
                position_latitude=float(house.lat.text),
                bedrooms=int(house.bedrooms.text),
                bathrooms=int(house.bathrooms.text),
                link=house.guid.text
            )
            houses.append(h)
        return houses
            