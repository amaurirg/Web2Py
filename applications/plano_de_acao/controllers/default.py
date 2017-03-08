# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

@auth.requires_login()
def index():
    return dict()


def planos_de_acao():
    # valida = ''
    # grid = SQLFORM.grid(PLANO)
    # return dict(grid=grid)
    # print db.plano.fields
    # filtro = SQLFORM.factory(
    #     Field( 'filtro', requires=IS_EMPTY_OR(IS_IN_DB(db, 'nome_ramal.id','%(nome)s - %(ramal)s',zero='RAMAL'))))
    planos = db(PLANO.concluido == 'NÃO').select(orderby=db.plano.prazo)
    concluidos = db(PLANO.concluido == 'SIM').select(orderby=db.plano.prazo)
    # print planos
    # print datetime.date.today()
    # return dict(planos=planos, concluidos=concluidos)


# def novo_plano():
    form = SQLFORM(PLANO, _id='form_novo_plano', submit_button='Salvar')
    if form.process().accepted:
        response.flash = "Salvo com sucesso!"
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
        # valida = 'erro'
    # else:
    #     response.flash = 'Preencha os campos para salvar ou alterar um plano de ação!'
    # form.add_button('Cancelar', URL('index'), _class='btn btn-primary')
    button = A('Cancelar', _href='index', _class="btn btn-primary", _style="border-radius: 5px;")
    # return dict(form=form)
    return dict(planos=planos, concluidos=concluidos, form=form, button=button)#, valida=valida)


def editar_plano():
    plano = db(PLANO.id == request.args(0, cast=int)).select().first()
    form = SQLFORM(PLANO, plano, submit_button='Salvar')
    if form.process().accepted:
        response.flash = 'Registro alterado com sucesso!'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    # else:
    #     response.flash = 'Nenhuma alteração foi realizada!'
    button = A('Cancelar', _href='../', _class="btn btn-primary", _style="margin-left:20px;border-radius: 5px;")
    return dict(form=form, plano=plano, button=button)


def ver_concluido():
    plano = db(PLANO.id == request.args(0, cast=int)).select().first()
    form = SQLFORM(PLANO, plano, submit_button='Salvar')
    if form.process().accepted:
        response.flash = 'Registro alterado com sucesso!'
    elif form.errors:
        response.flash = 'Erros no formulário!'
    # else:
    #     response.flash = 'Nenhuma alteração foi realizada!'
    button = A('Voltar', _href='../', _class="btn btn-primary", _style="margin-left:20px;border-radius: 5px;")
    return dict(form=form, plano=plano, button=button)


def export_xls():
    import openpyxl, os     #'''importa openpyxl'''
    from openpyxl import load_workbook
    #'''importa funções para converter letras e números'''
    # from openpyxl.cell import get_column_letter, column_index_from_string
    

    wb = load_workbook('./applications/plano_de_acao/static/files/PlanoAmauri.xlsx')
    sheet = wb.get_sheet_by_name('Plano')       #obtém a planilha Plan1
    sheet = wb['Plano']
    # anotherSheet = wb.active
    conteudo = sheet['A9']

    print sheet['B9'].value

    print 'Nome das planilhas: ', wb.get_sheet_names()

    print 'Valor: ', conteudo.value
    print 'Tamanho máximo de linhas da planilha: ', str(sheet.max_row)
    print 'Tamanho máximo de colunas da planilha: ', str(sheet.max_column)

    # print os.listdir('./applications/plano_de_acao/static/files')

    return "Leu arquivo xls"



def teste():
    return dict()


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


