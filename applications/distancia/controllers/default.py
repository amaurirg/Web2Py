# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import requests, time, json
from decimal import *


def index():

    def modoTransporte(escolha):
        if escolha == 'Carro': return 'mode=driving&departure_time=now&traffic_model=pessimistic'
        if escolha == 'Transporte público': return 'mode=transit&transit_mode=train|bus|subway'
        if escolha == 'Avião (em breve)': return 'mode=driving'
        
    res = ''
    tempo = ''
    distancia = '0'
    valorIda = 0
    valorTotal = 0
    dia = ''
    hora = ''
    minutos = ''
    form =  SQLFORM.factory(
    Field('origem', requires = IS_NOT_EMPTY(error_message='Digite o endereço da localidade.'), label='Localidade - ORIGEM:'),
    Field('destino', requires = IS_NOT_EMPTY(error_message='Digite o endereço da localidade.'), label='localidade - DESTINO:'),
    Field('transporte', label='Escolha o meio de transporte', widget=SQLFORM.widgets.radio.widget, 
            requires=IS_IN_SET(['Carro', 'Transporte público', 'Avião (em breve)'])),
    formstyle = 'divs',
    submit_button = 'Calcular'
    )
    form.element(_name='origem')['_id'] = 'searchTextField'
    form.element(_name='destino')['_id'] = 'searchTextField2'

    if form.process().accepted:
        meioTransporte = modoTransporte(form.vars.transporte)
        res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&%s&language=pt-BR&key=AIzaSyDYqS1ip-x52ERWpDhCbENLi7xMgCatm94'%(form.vars.origem, form.vars.destino, meioTransporte))                                 #chama a API do Google com a chave de servidor e armazena em "res".

        print res.raise_for_status()                                                   #melhor forma de verificar se houve erro no download.
        maps_data = json.loads(res.text)                                                #lê os dados json e armazena em "maps_data".
        trafValor = maps_data['rows'][0]['elements'][0]['duration_in_traffic']['value']        #seleciona os campos desejados e exibe na tela.
        #time.strftime('%H:%M:%S', time.gmtime(12345))
        tempo = time.gmtime(trafValor)
        dia = tempo[2]
        hora = tempo[3]
        minutos = tempo[4]
        distancia = maps_data['rows'][0]['elements'][0]['distance']['text']        #seleciona os campos desejados e exibe na tela.
        
        if form.vars.transporte == 'Transporte público':
            valorIda = maps_data['rows'][0]['elements'][0]['fare']['value']        #seleciona os campos desejados e exibe na tela.
            valorIdaVolta = valorIda * 2
            valorTotal = Decimal(valorIdaVolta).quantize(Decimal('1.00'))
        if form.vars.transporte == 'Carro':
            valorIda = maps_data['rows'][0]['elements'][0]['distance']['value']        #seleciona os campos desejados e exibe na tela.
            valorIdaVolta = round(((((valorIda*0.001)/8)*3.699)*2),2)
            valorTotal = Decimal(valorIdaVolta).quantize(Decimal('1.00'))
        print 'Tempo = ', tempo[2]
        print 'Tempo = ', tempo[3]
        print 'Tempo = ', tempo[4]
        # print 'Distância = ', distancia
        # print '\n', maps_data
        print '\n', res.text
        # print form.vars.origem
        # print form.vars.destino
        # print form.vars.transporte
        # print valorIda
        # print valorTotal
        # print type(valorIda)
        # print type(valorTotal)
    return dict(form=form, dia=dia, hora=hora, minutos=minutos, distancia=distancia, valorTotal=valorTotal)


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


