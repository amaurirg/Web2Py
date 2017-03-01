# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    # grid = SQLFORM.grid(PLANO)
    # return dict(grid=grid)
    planos = db(PLANO).select()
    print planos
    return dict(planos=planos)


def novo_plano():
    form = SQLFORM(PLANO, _class='form-control', submit_button='Salvar')
    if form.process().accepted:
        response.flash = "Salvo com sucesso!"
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    else:
        response.flash = 'Preencha os campos para salvar ou alterar um plano de ação!'
        form.add_button('Cancelar', URL('index'), _class='btn btn-primary')
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


