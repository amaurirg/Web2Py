# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

# gato    =   db.gatos.insert(nome=”Sr.   Pelinhos”,  raca=”Sphynx”)

def index():
    form = SQLFORM.factory(
        Field('sig', requires = IS_IN_DB(db, 'sigla_cidade.id', '%(sigla)s')),
        Field('nom', requires = IS_IN_DB(db, 'nome_cidade.id', '%(nome)s')))
    # form_nome_sigla = SQLFORM(SCNC)
    if form.process().accepted:
        print request.vars.sig, request.vars.nom
        SCNC.insert(nome_cid=request.vars.sig, sigla_cid=request.vars.nom)
    else:
        response.flash = 'ERRO'
    return dict(form=form)


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


