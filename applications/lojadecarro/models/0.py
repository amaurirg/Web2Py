# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite')
e_m = {
	'empty':'Este campo é obrigatório',
	'in_db':'Este registro já existe no banco de dados',
	'not_in_db':'Este registro já existe no banco de dados',
	'email':'Você precisa inserir um e-mail válido',
	'image':'O arquivo precisa ser uma imagem válida',
	'not_in_set':'Você precisa escolher um valor válido',
	'not_in_range':'Digite um número entre %(min)s e %(max)s',
}

config = dict(nmsite='Loja de Carro', dscsite='Só os melhores carros')

estados = ('Novo', 'Usado')

cores = ('Azul', 'Amarelo', 'Verde', 'Vermelho', 'Prata', 'Branco', 'Preto', 'Vinho')

from gluon.tools import Crud
crud = Crud(db)