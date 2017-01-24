from  bs4 import BeautifulSoup
from configparser import ConfigParser
import requests
import props_database
import re
from pony.orm import db_session
from pony.orm.core import TransactionIntegrityError

class DaftRss(object):
    '''
    Have API, is private.
    Conclusion: Fuck them
    '''
    def retrieve(self):
        config = ConfigParser()
        config.read('settings.ini')
        rss = config.get('daft', 'url')
        data = requests.get(rss)
        soup = BeautifulSoup(data.content, "lxml-xml")
        houses = []
        for house in soup.find_all('item'):
            h = None
            try:
                with db_session:
                    try:
                        h=self.parse_house(house)
                    except Exception:
                        print("Failed to parse:\n{}".format(house.prettify()))
            except TransactionIntegrityError:
                h = None # duplicate
            if h is not None:
                houses.append(h)
        return houses

    def parse_house(self, item): 
        g = re.match(r'([0-9,]+)\s+(\w+)', item.price.text)
        pr = 0
        if g is not None:
            pr = float(g.group(1).replace(',',''))
            if g.group(2) == 'weekly':
                pr = pr * 4
        baths = item.bathrooms
        if baths is None:
            baths = 0
        else:
            baths =  item.bathrooms.text
        img = ''
        soup2 = BeautifulSoup(item.description.text, 'lxml')
        if soup2.img:
            img = soup2.img.attrs['src']
        h = props_database.Property(
            title=item.title.text,
            description=item.description.text,
            price=pr,
            price_string=item.price.text,
            main_photo=img,
            address=item.address.text,
            position_longitude=float(item.long.text),
            position_latitude=float(item.lat.text),
            bedrooms=int(item.bedrooms.text),
            bathrooms=int(baths),
            link=item.guid.text
        )
        return h
            