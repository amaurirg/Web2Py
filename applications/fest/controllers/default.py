# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
'''
SEC_ATENDIMENTO
SEC_CAIXA
SEC_CORPORATIVO
SEC_DIRETORIA
SEC_ESTECH
SEC_ESTOQUE
SEC_FINANCEIRO
SEC_LICITAÇÃO
SEC_LOJA
SEC_RH
SEC_TI
SEC_VENDAS
SEC_WEB
'''

#@auth.requires_login()
def index():
    num_ramal = '' 
    form =  SQLFORM.factory(
        Field('keyword', requires = IS_NOT_EMPTY(error_message=''), label='Buscar por nome, ramal ou departamento'),
        formstyle = 'divs',
        submit_button = 'Localizar'
        )
    response.flash = 'Digite um nome ou ramal para a localização!'
    if form.process().accepted:
        num_ramal = db(NR.nome.like('%'+form.vars.keyword+'%')).select() | db(NR.ramal.like(form.vars.keyword)).select() | db(NR.depto.like('%'+form.vars.keyword+'%')).select()
        if not num_ramal:
            response.flash = 'Ramal não encontrado!' 
        else:
            response.flash = 'Ramal localizado!'
    elif form.errors:
        response.flash = 'O campo deve ser preenchido!'        
    #exp = db.export_to_csv_file(open('meu_banco2.csv', 'wb'))
    #button = A('Relatório de Chamadas', _href='chamadas_diarias', _class="btn")
    return dict(form=form,num_ramal=num_ramal)#, exp=exp)
    

#@auth.requires_membership('user_ramais')
def novo_ramal():
    form = SQLFORM(NR, formstyle = 'divs', submit_button = 'Cadastrar')
    if form.process().accepted:
        response.flash = 'Ramal criado com sucesso!'
        redirect(URL('user/logout'))
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    else:
        response.flash = 'Preencha os campos para cadastrar um novo ramal!'
    form.add_button('Voltar para Página Principal', URL('user/logout'), URL('index'))
    return dict(form=form)


#@auth.requires_membership('user_ramais')
def atualizar_ramal():
    novo = db(NR.id == request.args(0)).select().first()
    response.flash = ''
    form = SQLFORM(NR, novo, formstyle = 'divs', submit_button = 'Alterar Ramal')
    if form.process().accepted:
        response.flash = 'Ramal alterado com sucesso!'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    else:
        response.flash = 'Preencha os campos para alterar um ramal!'
    form.add_button('Voltar para Página Principal', URL('user/logout'), URL('index'))
    return dict(form=form)


'''
def contato():
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY(), label='Nome'),
        Field('email', requires=IS_EMAIL(), label='Email'),
        Field('message', 'text', requires=IS_NOT_EMPTY(), label='Mensagem'),
        formstyle='divs',
        submit_button='Enviar'
        )
    if form.process().accepted:
        mail.send(to=['amaurirg@terra.com.br'],
            subject='Chamado-Dúvida',
            reply_to=form.vars.email,
            message="""<html>
            <strong>Novo chamado</strong><br>
            %(name)s enviou a seguinte mensagem: <br>
            %(message)s
            </html>"""%{'name':form.vars.name,'message':form.vars.message}
            )

    form.add_button('Home', URL('index'))
    return dict(form=form)
'''

### CONTROLLER

def sendmail():
    result = mail.send('agiovani@estech.com.br','Testando','Olá estou testando o email')
    return result

def email():
    dados = db(REC.id).select().last()
    data = str(dados.created_on)
    data_completa = data[8:10] + '/' + data[5:7] + '/' + data[0:4]
    hora = data[11:]
   
    for row in db(db.auth_user.id==dados.created_by).select():
        nome_completo = str(row.first_name) + ' ' + str(row.last_name)

    for other_row in db(TIPO.id==dados.status).select():
        tipo = str(other_row.tipo_status)

    for more_other_row in db(NR.id==dados.ramal).select():
        destinatario = more_other_row.email

    confirm = mail.send(to=[destinatario],
        subject='Recado',
        message="""<html>
        <p><b>%(nome)s</b> entrou em contato. </p><br />
        Mensagem: %(mensagem)s <br /><br />
        Observações: %(obs)s <br /> <br />
        Nome: %(nome)s <br />
        Telefone: %(tel)s <br />
        Empresa: %(emp)s <br />
        Produto de interesse: %(prod)s <br />
        Status: %(status)s <br />
        Atendente: %(atend)s <br />
        Data da chamada: %(dc)s <br />
        Hora da chamada: %(hc)s <br />
        </html>"""%{'nome':dados.nome,'mensagem':dados.msg, 'tel':dados.tel, 'emp': dados.emp,\
        'prod':dados.prod, 'status':tipo, 'obs':dados.obs, 'atend':nome_completo, 'dc':data_completa, 'hc':hora}
        )
    if confirm:
        envio = 'Email enviado com sucesso!'
        redirect(URL('recepcao'))
    else:
        envio = 'ERRO NO ENVIO DO EMAIL'
    return dict(envio=envio)


#@auth.requires_login()
#@auth.requires_membership('user_recepcao')
def recepcao():
    dados = db(CONF.sel).select()

    form = SQLFORM(REC, formstyle = 'divs', submit_button = 'Salvar Chamada')
    
    if form.process().accepted:
        print form.vars.env
        if form.vars.env == '2':
            redirect(URL('email'))
        elif form.vars.env == '1':
            redirect(URL('recepcao'))
        else:
            redirect(URL('index'))
    button = A('Relatório de Chamadas', _href='chamadas_diarias', _class="btn")
    return dict(form=form, dados=dados, button=button)


def chamadas_diarias():
    form = SQLFORM.factory(
              Field( 'name', requires=IS_EMPTY_OR(IS_IN_DB(db, 'nome_ramal.id','%(nome)s - %(ramal)s',zero='RAMAL'))),
              Field('Data_Ini',  'date',requires=IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y', error_message='O formato deve ser DD/MM/AAAA'))),
              Field('Data_Fim',  'date',requires=IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y', error_message='O formato deve ser DD/MM/AAAA'))),  
              submit_button='Gerar relatório')

    if form.process().validate:
        inicio = str(form.vars.Data_Ini)
        fim = str(form.vars.Data_Fim)
        if (form.vars.name != None) & (form.vars.Data_Ini != None) & (form.vars.Data_Fim != None):
            diarias = db((db.recepcao.created_on>=inicio) & (db.recepcao.created_on<=fim) & (db.recepcao.ramal.like(str(form.vars.name)))).select()
            ramal_selecionado = db(NR.id==form.vars.name).select().first()
            rs = ramal_selecionado.nome+' - '+ramal_selecionado.ramal
            return dict(form=form,diarias=diarias,lbl='',ramal_sel='RAMAL SELECIONADO: '+rs, data_inicial='PERÍODO: '+inicio,data_final=' à '+fim)
        elif (form.vars.name == None) & (form.vars.Data_Ini != None) & (form.vars.Data_Fim != None):
            diarias = db((db.recepcao.created_on>=inicio) & (db.recepcao.created_on<=fim)).select()
            return dict(form=form,diarias=diarias, lbl='',ramal_sel='RAMAL SELECIONADO: Todos os ramais', data_inicial='PERÍODO: '+inicio,data_final=' à '+fim)
        elif (form.vars.name != None) & (form.vars.Data_Ini == None) & (form.vars.Data_Fim == None):
            diarias = db(db.recepcao.ramal.like(str(form.vars.name))).select()
            ramal_selecionado = db(NR.id==form.vars.name).select().first()
            rs = ramal_selecionado.nome+' - '+ramal_selecionado.ramal
            return dict(form=form,diarias=diarias, lbl='',ramal_sel='RAMAL SELECIONADO: '+rs,data_inicial='PERÍODO: Todas as datas',data_final='')
        else:
            lbl = H4('Preencha os campos para gerar o relatório!', _class='test', _id=0)
            return dict(form=form,diarias='', lbl=lbl,ramal_sel='', data_inicial='',data_final='')


# ramal_selecionado = db(NR.id==form.vars.name).select().first()
# ramal_selecionado.nome+' - '+ramal_selecionado.ramal_sel

        # print 'form.vars.name = ',form.vars.name
        # print 'form.vars.Data_Ini = ',form.vars.Data_Ini
        # print 'form.vars.Data_Fim = ',form.vars.Data_Fim

        #     diarias = db((db.recepcao.created_on.like(str(form.vars.Data_Ini)+'%')) | (db.recepcao.ramal.like(str(form.vars.name)))).select()
        # elif  (form.vars.name == None) & ((form.vars.Data_Ini != None) & (form.vars.Data_Fim != None)):
        
        # else:
        #     diarias = db((db.recepcao.created_on.like(str(form.vars.Data_Ini)+'%')) & (db.recepcao.ramal.like(str(form.vars.name)))).select()
        
    #return dict(form=form)

#periodo = db.executesql("select recepcao.created_on from recepcao where recepcao.created_on between %s(inicio)s and %s(fim)s"%{'inicio':inicio,'fim'=fim})
#select db.recepcao.created_on from db.recepcao where db.recepcao.created_on between form.vars.Data_Ini and form.vars.Data_Fim
#("select recepcao.created_on from recepcao where recepcao.created_on between '2015-03-01' and '2015-04-30'")
def lista_completa_de_ramais():
    todos_ramais = db(NR).select(orderby=NR.ramal)
    return dict(todos_ramais=todos_ramais)


def erro():
    return dict()


def aluno():
    agora = request.now
    return dict(nome='Fulano', curso='web2py', idade=27, dia=agora.date(), hora=agora.time())


def data():
    dados = db(REC.id).select().last()
    data = str(dados.created_on)
    data_completa = data[8:10] + '/' + data[5:7] + '/' + data[0:4]
    hora = data[11:]
    print 'Data = ', data_completa, 'Hora = ', hora

    '''
    data_atual = str(datetime.date.today())
    ano = data_atual[0:4]
    mes = data_atual[5:7]
    dia = data_atual[8:10]
    print ano
    print mes
    print dia
    '''


def user5():
    form = auth()
    return dict(form=form)


def teste():
    db(NR.nome>24).delete()
    return dict()


def banco():
    for row in db(db.auth_user.id==2).select():
        nome_completo = str(row.first_name) + ' ' + str(row.last_name)
    return dict(nome_completo=nome_completo)


def banco2():
    dados = db().select(REC.status)
    return dict(dados=dados)


def banco3():
    dados = db(REC.id==1).select(REC.emp)
    return dict(dados=dados)


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
    response.flash = 'Preencha os campos para acessar o sistema'
    auth.settings.remember_me_form = False
    #auth.messages.access_denied = 'Você não tem essa permissão!'
    #auth.messages.label_remember_me = "Lembrar-me"
    
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


#@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)



'''
def rel_valores():
    report = local_import('Report',reload=True)
    response.subtitle = 'Relatório de Valores'
    response.view = 'rel_valores.html'
   
    form = SQLFORM.factory(Field('data_ini', 'date', label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                           Field('data_fim', 'date', label='Data final',
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')),
                                 submit_button='Enviar')
    pdf_link=FORM(INPUT(_type='submit',_value='PDF'),
                      hidden=dict(data_ini=request.vars.data_ini,data_fim=request.vars.data_fim),
                      _action='rel_valores.pdf',
                      submit_button='Enviar')
    if request.extension=='pdf' or form.accepts(request.vars, session):
        data_ini = request.now.strptime(request.vars.data_ini, '%d/%m/%Y')
        data_fim = request.now.strptime(request.vars.data_fim, '%d/%m/%Y')
        fluxo = db((db.cadvalores.dtpagto >= data_ini) &
                   (db.cadvalores.dtpagto <= data_fim)).select(db.cadvalores.dtpagto,
                                                       db.cadvalores.basecalc,
                                                       groupby=db.cadvalores.dtpagto|db.cadvalores.basecalc)
        tbl = report.ReportTable(rows=fluxo,
                      grouping={'field':'cadvalores.dtpagto', 'function': lambda row: row.dtpagto.month},
                      sumary={'cadvalores.basecalc': lambda row,v: (v-row.basecalc,v+row.basecalc)[row.basecalc=='Base Calc']},
                     footer={'cadvalores.basecalc': lambda row,v: (v-row.basecalc,v+row.basecalc)[row.basecalc=='Base Calc']},
                     col_widths=[15,11,50,10,10],  
                     truncate=50              
                    )
        if request.extension=='pdf':
            pdf = Relatorio()
            pdf.add_page()
            pdf.write_html(tbl.generate().xml().decode('UTF-8'))
            response.headers['Content-Type'] = 'application/pdf'
            return pdf.output(dest='S')
        else:
           return dict(form=form, rel=tbl.generate(),pdf_link=pdf_link)
    else:
       return dict(form=form, rel='Informe as datas limites',pdf_link=None)

'''