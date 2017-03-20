SC = db.define_table('sigla_cidade',
	Field('sigla', length=2),
	format = '%(sigla)s'
	)

NC = db.define_table('nome_cidade',
	Field('nome'),
	format = '%(nome)s'
	)

SCNC = db.define_table('nome_sigla_cidade',
	Field('sigla_cid', 'reference sigla_cidade'),
	Field('nome_cid', 'reference nome_cidade'),
	format = '%(nome_cid)s - %(sigla_cid)s'
	)



NOVA = db.define_table('nova',
	Field('sc'),
	Field('nc'),
	format='%(novatab)s'
	)