# -*- coding: utf-8 -*-

#NR (Nome-Ramal)
NR.nome.requires = IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'nome_ramal.nome')
NR.depto.requires = IS_NOT_EMPTY()
NR.ramal.requires = IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'nome_ramal.ramal')
NR.email.requires = IS_NOT_EMPTY()


#TIPO
TIPO.tipo_status.requires = IS_NOT_EMPTY()

#REC (Recepção)
REC.nome.requires = IS_NOT_EMPTY()
REC.tel.requires = IS_NOT_EMPTY()
REC.ramal.requires = IS_IN_DB(db,'nome_ramal.id', '%(nome)s - %(ramal)s', zero='RAMAL SOLICITADO')
REC.status.requires = IS_IN_DB(db,'lista_status.id', '%(tipo_status)s', zero = 'STATUS')
REC.env.requires = IS_IN_DB(db,'env_email.id', '%(sel)s', zero = None)


