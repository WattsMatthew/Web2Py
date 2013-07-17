# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
""" This default controller function for index.html
    INPUT: Nothing
    OUTPUT:Redirection
    ACTION:Redirect to login, about and rules page

"""
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to PyPro 2013!")
    return dict(message=T('print>>Hello World'))



""" This is controller function for login.html
    INPUT: username and password
    OUTPUT: Redirect to user's home page.
    ACTION: A) Check whether username is exist or not
             1) If yes then check password
                if
             2) If not then register username and password.
                redirect to options.html for choosing level
"""
def login():
    form=FORM(TABLE(TR('Username ',
              INPUT(_name='username',_type='string',requires=IS_NOT_EMPTY())),
              TR('Password ',
              INPUT(_name='password',_type='password',requires=IS_NOT_EMPTY())),
              TR(INPUT(_type='Submit',_value='Go'))
               ),_method='post'              
              )
    #storing all data into session
    session.start=True
    session.username=request.vars.username
    session.password=request.vars.password
        
    #To check all fields are filled
    if form.accepts(request,session):
        #check whether username is present or not
        get_password=db(db.Programmer.username==request.vars.username).select(db.Programmer.password,db.Programmer.level)
        #checking retrieved password is null or not if it is not null then user is registered already
        if len(get_password):
            #Checking user entered password with the database
            if get_password[0]['password']==request.vars.password:
                #response.flash="Login successful!!!"
                redirect(URL('home.html'))
            else:
                #if password doesn't match with database then we've show a message
                response.flash="Username is exist or wrong password"
        else:
            #means data isn't exist for that 'username' so we've to register it
            db.Programmer.insert(username=request.vars.username,password=request.vars.password,level=1)
            db.commit()
            redirect(URL('options.html'))
            #end of the registration
    elif form.errors:
        response.flash="Form has errors"
    else:
        response.flash="Please fill the username and password" 
        
    return dict(form=form)

"""
    This is a controller function
    INPUT: valid username,level selection from level['Not specified','Beginner','Intermediate','Expert']
    OUTPUT:Updation of level
    ACTION:User has to select appropriate level according to his skills

"""
def options():
    get_level=0
    form=FORM(TABLE(TR(B('Level: '),SELECT('Beginner','Intermediate','Expert',_name='level')),
                    TR(INPUT(_type='submit',_value='Done'))))
    #Getting index from list level=['Not specified','Beginner','Intermediate','Expert']
    #level list is defined in db.py
    if form.accepts(request,session):
        if request.vars.level in level:
            get_level=level.index(request.vars.level) + 1
        else:
            request.vars.level=1
    #doing updation
        db(db.Programmer.username==session.username).update(level=get_level)
        session.userlevel=get_level
        #Finding user ID
        get_id=db(db.Programmer.username==session.username).select(db.Programmer.id)
        if len(get_id):
            userid=get_id[0]['id']
        redirect(URL('home.html'))
    return dict(form=form)




""" This function is controller for home.html
    INPUT: authorized username and password
    OUTPUT:Display activites and redirect them according to user's action
    ACTION:upload file,change password,change level,check status
"""
def home():
    response.flash="Welcome," + session.username
    
    return dict()

def upload_data():
    db.Result.user_id.writable=db.Result.user_id.readable=False
    #db.Result.
    db.Result.status.writable=db.Result.status.readable=False
    form=SQLFORM(db.Result)
    if form.accepts(request,session):
        response.flash=form.vars
    else:
        response.flash="Error"
    return dict(form=form)
