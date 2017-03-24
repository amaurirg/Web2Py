SC = db.define_table('siglas',
	Field('sigla', length=2),
	format = '%(sigla)s'
	)