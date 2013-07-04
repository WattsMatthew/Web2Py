#Creating database connection with sqlite database.
db_connect=DAL('mysql://root:root@localhost/test')
#db_connect=DAL('sqlite://storage.db')

#Define schema for parent and child tables
db_connect.define_table('Parent',
                        Field('name',unique=True,notnull=True),format='%(name)s',migrate=False)

db_connect.define_table('Child',
                        Field('cname',notnull=True,length=120),
                        Field('mother',type='reference Parent'),
                        Field('father',type='reference Parent'),format='%(name)s',migrate=False)

#Inserting record in Parent table.
#db_connect.Parent.bulk_insert([{'name':'Bob'},{'name':'Alice'},{'name':'Mary'},{'name':'Peter'}])
#Inserting record in Child table.
#db_connect.Child.bulk_insert([{'cname':'John','mother':'2','father':'1'},{'cname':'Jane','mother':'3','father':'4'}])
