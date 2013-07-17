#Creating connection with SQLite Database
db=DAL("sqlite://storage.db")
#Defining table Level
db.define_table('Level',
                Field('name',unique=True),
                format='%s(name)s',
                migrate='Level.table'
                )
db.define_table('Programmer',
                Field('username',unique=True),
                Field('password',type='password',notnull=True),
                Field('level','reference Level',notnull=True),
                format='%(username)s',
                migrate='Programmer.table'
                )

db.define_table('Programs',
                Field('problem_statement',notnull=True),
                Field('level','reference Level',notnull=True),
                format='%(problem_statement)s',
                migrate='Programs.table'
                )

db.define_table('Admin',
                Field('admin_name',unique=True),
                format='%(admin_name)s',
                migrate='Admin.table'
                )

db.define_table('Result',
                Field('user_id','reference Programmer'),
                Field('programs_id','reference Programs'),
                Field('solution','upload'),
                Field('status',default='Pending'),
                Field('remarks',default='none'),
                format='%(status)s',
                migrate='Result.table'
                )
                

level=['Not Specified','Beginner','Intermediate','Expert']


"""db.define_table('Status',
                Field('problem_statement','reference Programs')
"""

""" ###Inserting data into Level####
    for x in level:
       db.Level.insert(name=x)
       
   ####Inserting data into Programs###
   for x in range(100):
       db.Programs.insert(problem_statement="Problem statement No " + str(x),level=1)
       ### just have to change level=2 and 3 for adding programs to next leve
"""
