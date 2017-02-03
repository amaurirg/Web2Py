# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import requests, json

def index():
   
    return dict()


def form():
    form = SQLFORM.factory(Field('texto'), submit_button='Buscar')
    print "http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s" %request.vars.texto
    return dict(form=form)

def redpython():
    # print "http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s" %request.vars.texto
    # return dict()
    # form = SQLFORM.factory(Field('texto'), submit_button='Buscar')
    # print "http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s" %request.vars.texto
    # return dict(form=form)
    resp, retorno, lista, qtde = '', '', '', ''
    if request.vars:
        resp = requests.get("http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s" 
                            %request.vars.texto)
        retorno = json.loads(resp.text)
        print "http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s" %request.vars.texto
        # for row in retorno['videos']:
        #     print row['video']['title']
        if retorno['count'] != 0:
            lista = [row['video'] for row in retorno['videos']]
            qtde = "Foram encontrados %s vídeos" %retorno['count']
    # return resp
    # print request.args
        # print(resp.text)
    return dict(resp=resp, retorno=retorno, qtde=qtde, lista=lista)

    

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


