db = DAL('sqlite://storage.sqlite')

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('alarm',
    Field('name'),
    Field('date'),
    Field('time'),
    format='%(name)s')