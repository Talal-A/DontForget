# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


db = DAL('sqlite://storage.sqlite')
#user authorization stuff
auth = Auth(db)
auth.define_tables()
#crud = Crud(db)

db.define_table('alarm',
                Field('name'),
                Field('phone_number'),
                Field('carrier'),
                Field('email_address'),
                Field('reminder_date', 'date'),
# not needed yet                Field('reminder_time'),
                Field('reminder_message', 'text'))


#will require enter a time of the form HH:MM:SS
#db.alarm.time.requires = IS_TIME()



#default fields
#if user is signed on will auto fill the fields else typical messages
if auth.user:
    db.alarm.name.default = auth.user.first_name
    db.alarm.email_address.default= auth.user.email
else:
    db.alarm.name.requires = IS_NOT_EMPTY(error_message = "Please enter your name")
    db.alarm.email_address.requires = IS_EMAIL(error_message = "Please enter a"
        " valid email address")

# Validation
db.alarm.reminder_date.requires = IS_DATE(format=T('%Y-%m-%d'), error_message = "Must be YYYY-DD-MM")
db.alarm.phone_number.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
         error_message='Must be 1-XXX-XXX-XXXX.')

db.alarm.carrier.requires = IS_IN_SET(['ATT', 'Verizon', 'T-Mobile', 'Sprint',
        'Other'])


#authentication

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=False,signature=False)

#from gluon.contrib.login_methods.rpx_account import RPXAccount
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
#auth.settings.login_form = RPXAccount(request,
#    api_key='630fd1d1ed78383c889a5809d54fd1ea27da907d',
#    domain='https://dontforget.rpxnow.com/',
#    url = "http://dontforget.rpxnow.com/%s/default/user/login" % request.application)