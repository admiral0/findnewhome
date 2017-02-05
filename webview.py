from bottle import route, run, template
import humanize
from props_database import db_connect, Property
from pony.orm import db_session,select

TEMPLATE='''
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
</head>
<body>
<table>
<tr>
<td>id</td>
<td>address</td>
<td>price</td>
<td>bike</td>
<td>transit</td>
<td>transport</td>
<td>wake_up</td>
% import humanize
</tr>
<% for p in props: %>
<tr>
<td><a href='{{p.link}}'>{{p.ad_id}}</a></td>
<td>{{p.address}}</td>
<td>{{p.price_string}}</td>
<td>{{humanize.naturaldelta(p.by_bicycle)}}</td>
<td>{{humanize.naturaldelta(p.by_transit)}}</td>
<td>{{'luas ' if p.transit_luas else ''}}{{'dart' if p.transit_dart else ''}}</td>
<td>{{p.by_transit_start}}</td>
</tr>
<% end %>
</table>
</body>
</html>
'''

db_connect()

@route('/1')
@db_session
def index():
    res = select(p for p in Property).order_by(Property.by_bicycle)[:50]
    return template(TEMPLATE, {
        'title': 'Ordered by bike',
        'props': res
    })

@route('/2')
@db_session
def index2():
    res = select(p for p in Property).order_by(Property.by_transit)[:50]
    return template(TEMPLATE, {
        'title': 'Ordered by bike',
        'props': res
    })


run(host='localhost', port=8080)