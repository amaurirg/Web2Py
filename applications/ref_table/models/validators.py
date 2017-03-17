SC.sigla.requires = IS_IN_DB(db, 'sigla_cidade.id', '%(sigla)s', zero = 'SIGLA')
NC.nome.requires = IS_IN_DB(db, 'nome_cidade.id', '%(nome)s', zero = 'NOME')
