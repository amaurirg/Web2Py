# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import random

"""
lista = ['A', 'B', 'C', 'D']

lista_jogos = []

for i,item in enumerate(lista):
    for item in lista:
        if lista.index(item) == i:
            continue
        else:
            jogo = sorted([lista[i], item])
            if not jogo in lista_jogos:
                lista_jogos.append(jogo)
print(lista_jogos)

random.shuffle(lista_jogos)
print(lista_jogos)
"""

def jogos():
    grid = SQLFORM.grid(CLUBES)
    times = db(CLUBES).select(CLUBES.clube)
    # print times
    lista = []
    for item in times:
        lista.append(item.clube)
        # print item.clube
    # lista = [x for x in times]
    # print lista
    lista_jogos = []

    for i,item in enumerate(lista):
        for item in lista:
            if lista.index(item) == i:
                continue
            else:
                jogo = sorted([lista[i], item])
                if not jogo in lista_jogos:
                    lista_jogos.append(jogo)
    # print(lista_jogos)

    # random.shuffle(lista_jogos)
    # print(lista_jogos)

    # return dict()
    return dict(grid=grid, lista_jogos=lista_jogos, times=times)


def index():
    dados = db(CLUBES.clube=="Palmeiras").select(CLUBES.pontos)
    for dado in dados:
        res = int(dado.pontos)
    return res + 3


def teste_classe():

    class Equipes:
        # docstring for Equipes
        pontos = 0
        gols = 0
        def __init__(self, nome, equipe):
            self.nome = nome
            self.equipe = equipe



    thiago = Equipes("Thiago", "França")
    bruno = Equipes("Bruno", "Portugal")
    fernanda = Equipes("Fernanda", "Brasil")
    amauri = Equipes("Amauri", "Alemanha")

    print thiago.equipe

    nomes = [thiago, fernanda, bruno, amauri]

    # print nomes
    
    equipes = [clube.equipe for clube in nomes]

    print equipes
    # nomes = [thiago.equipe, fernanda.equipe, bruno.equipe, amauri.equipe]

    # print(jogo1.gols_marcados)

    # for time in nomes:
    #     print time.nome, time.equipe, time.pontos, time.gols

    lista_jogos = []


    for i,item in enumerate(equipes):
        for item in equipes:
            if equipes.index(item) == i:
                continue
            else:
                jogo = sorted([equipes[i], item])
                if not jogo in lista_jogos:
                    lista_jogos.append(jogo)

    print "lista_jogos", lista_jogos

    # jogos = {'jogo1':{thiago.equipe:thiago.gols, amauri.equipe:amauri.gols}}

    # print jogos['jogo1']


    # thiago.gols = 6
    # amauri.gols = 4

    # jogos = {'jogo1':{thiago.equipe:thiago.gols, amauri.equipe:amauri.gols}}

    # if thiago.gols > amauri.gols:
    #     thiago.pontos += 3
    # elif thiago.gols < amauri.gols:
    #     amauri.pontos += 3
    # else: 
    #     amauri.pontos += 1
    #     thiago.pontos += 1


    # print 'Equipe',jogos['jogo1'][thiago.equipe]

    # print jogos['jogo1']

    # print jogos

    # for time in nomes:
    #     print time.nome, time.equipe, time.pontos, time.gols


    return dict(lista_jogos=lista_jogos)

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


