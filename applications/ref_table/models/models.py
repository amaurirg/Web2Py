SC = db.define_table('sigla_cidade',
	Field('sigla'),
	format = '%(sigla)s'
	)

NC = db.define_table('nome_cidade',
	Field('nome'),
	format = '%(nome)s'
	)

SCNC = db.define_table('nome_sigla_cidade',
	Field('nome_cid'),
	Field('sigla_cid'),
	format = '%(nome_cid)s - %(sigla_cid)s'
	)