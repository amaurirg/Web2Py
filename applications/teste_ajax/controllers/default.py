# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    return dict()


def new_post():
    form = SQLFORM(db.post)
    if form.accepts(request, formname=None):
        return DIV("Message posted")
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])


def data():
    if not session.m or len(session.m)==10: session.m=[]
    if request.vars.q: session.m.append(request.vars.q)
    session.m.sort()
    return TABLE(*[TR(v) for v in session.m]).xml()


def func_teste():
    if request.vars.your_message:
        return request.vars.your_message

def month_input():
    return dict()

def month_selector():
    if not request.vars.month: return ''
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September' ,'October',
              'November', 'December']
    month_start = request.vars.month.capitalize()
    selected = [m for m in months if m.startswith(month_start)]
    return DIV(*[DIV(k,
                     _onclick="jQuery('#month').val('%s')" % k,
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for k in selected])
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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


