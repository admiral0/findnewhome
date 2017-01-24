#!/usr/bin/env python

from commute import GoogleDistance
from websites.daftie import DaftRss
from props_database import db_connect, Property
from pony.orm import select, db_session

db_connect()
rss=DaftRss()
rss.retrieve()

g = GoogleDistance()

with db_session:
    for pr in select(p for p in Property if p.by_transit is None):
        g.commute_work_transit(pr)
        g.commute_work_bicycle(pr)