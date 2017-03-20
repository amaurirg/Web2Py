# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

# gato    =   db.gatos.insert(nome=”Sr.   Pelinhos”,  raca=”Sphynx”)
# rows = db(query).select()
# >>> rows_list = rows.as_list()
def indexx():
    # siglas = db(SC).select()
    # lista = [sig.sigla for sig in siglas]
    # lista = [sig.sigla for sig in db(SC).select()]

    dados = db(NOVA.nc=='RJ').select()
    form3=''
    # form3 = SQLFORM.factory(
    # #     Field('sig', requires = IS_IN_DB(db, 'sigla_cidade.id', '%(sigla)s')),
    #     Field('sig', requires = IS_IN_SET([sig.sigla for sig in db(SC).select(SC.sigla)])),
    #     Field('nom', requires = IS_IN_SET([nom.nome for nom in db(NC).select(NC.nome)])))
    #     Field('nom', requires = IS_IN_DB(db, 'nome_cidade.id', '%(nome)s')))
    form = SQLFORM(SCNC)
    # form2 = SQLFORM.factory(Field('campo', requires=IS_IN_SET(NC.fields)))

    if form.process().accepted:
        response.flash = 'Salvo'
        # print 'request.vars.sig', request.vars.sig, request.vars.nom
        # SCNC.insert(nome_cid=request.vars.sig, sigla_cid=request.vars.nom)
        # NOVA.insert(nc=request.vars.nom, sc=request.vars.sig)
    else:
        response.flash = 'ERRO'

    # filtro = SQLFORM.factory(Field('filter', requires = IS_IN_SET([nom.nome for nom in db(NC).select(NC.nome)])))
    # if filtro.process().accepted:
    #     cidades = db(NOVA.nc==request.vars.filter).select(NOVA.nc, NOVA.sc)
    # else:
    #     cidades = ''
    filtro=''
    cidades=''
    cids=''
    filtra_campo = SQLFORM.factory(Field('field_filter', requires = IS_IN_SET(NOVA.fields)))
    if filtra_campo.process().accepted:
        # a = 'NOVA.%s'%request.vars.field_filter
        # a = NOVA.

        # ===============>   TENTAR FAZER COM NOVA.fields==request.vars.field_filter   <==============================

        # cids = db(NOVA).select(a)#request.vars.field_filter)
        print cids
    else:
        cids = ''
        print cids

    # print filtra_campo
    # print db._timings       # mostra todas as queries e o tempo de execução

    return dict(form=form, form3=form3, dados=dados, filtro=filtro, filtra_campo=filtra_campo, cidades=cidades, cids=cids)

# def teste():
#     return dict(message="BLAH")

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
    if request.args(0) == "register":
        hidden_fields = ['email']
        for field in hidden_fields:
            db.auth_user[field].writable = db.auth_user[field].readable = False

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


