SCNC.sigla_cid.requires = IS_IN_DB(db, 'sigla_cidade.id', '%(sigla)s', zero = 'SIGLA')
SCNC.nome_cid.requires = IS_IN_DB(db, 'nome_cidade.id', '%(nome)s', zero = 'NOME')
NOVA.usuario.readable = NOVA.usuario.writeable = False