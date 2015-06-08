# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from cStringIO import StringIO
import csv

class CSVExporter(object):
    """This class is used when grid's table contains reference key id.
       Exported CSV should contain reference key name of reference
       key not ids"""
    file_ext = "csv"
    content_type = "text/csv"

    def __init__(self, rows):
        self.rows = rows

    def export(self):
        if self.rows:
            s = StringIO()
            csv_writer = csv.writer(s)
            # obtain column names of current table
            col = self.rows.colnames
            # col contains list of column names
            # e.g: ["employee.id", "employee.name",
            #       "employee.email", "employee.company"]
            # get only attribute names i.e id, name, email, company
            heading = [c.split('.')[-1].upper() for c in col]
            # Write explicitly the heading in CSV
            csv_writer.writerow(heading)
            # don't write default colnames
            self.rows.export_to_csv_file(
                s, represent=True, write_colnames=False)
            return s.getvalue()
        else:
            return ''


@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    query = (db.employee.id > 0)
    # show only CSV and disable other formats.
    # call custom CSVExporter class.
    export_classes = dict(csv=(CSVExporter, 'CSV'), json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    # skip COMPANY column if request.vars._export_type exist
    if request.vars._export_type:
        fields = [db.employee.id, db.employee.name, db.employee.email]
    else:
        fields = [db.employee.id, db.employee.name, db.employee.email,
                  db.employee.company]
    grid = SQLFORM.grid(query, fields=fields, showbuttontext=False,
                        exportclasses=export_classes)
    return dict(grid=grid)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
