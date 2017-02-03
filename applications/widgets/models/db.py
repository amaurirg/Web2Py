# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)              # authentication/authorization
crud=Crud(globals(),db)              # for CRUD helpers using auth
service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc

# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None

auth.settings.hmac_key='sha512:ffc25cdd-3ed0-4e22-9cd2-f8e914c9222d'
auth.define_tables()                 # creates all needed tables

db.define_table('state',
                Field('name'),format='%(name)s')
db.define_table('city',
                Field('name'),
                Field('state',db.state),format='%(name)s')
db.define_table('zipcode',
                Field('value'),
                Field('city',db.city),format='%(value)s')
db.define_table('things',Field('name'),
                         Field('created_on','date'),
                         Field('value','integer',default=100),
                         Field('location',db.zipcode),
                         Field('rating',requires = IS_IN_SET(range(0,5)), default=1),
                         Field('stuff', requires = IS_IN_SET(['Apples','Oranges','Bananas','Kiwis','Lemons'],multiple=True)))

db.state.truncate()
db.city.truncate()
db.zipcode.truncate()
db.things.truncate()

db.state.insert(name='Texas')
db.state.insert(name='Illinois')
db.state.insert(name='California')

db.city.insert(name='Austin',state=1)
db.city.insert(name='Dallas',state=1)
db.city.insert(name='Chicago',state=2)
db.city.insert(name='Aurora',state=2)
db.city.insert(name='Los Angeles',state=3)
db.city.insert(name='San Diego',state=3)

db.zipcode.insert(value='78704',city=1)
db.zipcode.insert(value='78745',city=1)
db.zipcode.insert(value='75001',city=2)
db.zipcode.insert(value='75038',city=2)
db.zipcode.insert(value='60606',city=3)
db.zipcode.insert(value='60607',city=3)
db.zipcode.insert(value='60504',city=4)
db.zipcode.insert(value='60505',city=4)
db.zipcode.insert(value='90005',city=5)
db.zipcode.insert(value='90006',city=5)
db.zipcode.insert(value='92101',city=6)
db.zipcode.insert(value='92102',city=6)
    
from gluon.contrib.populate import populate
populate(db.things,20)
