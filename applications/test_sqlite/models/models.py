SC = db.define_table('siglas',
	Field('sigla', length=10),
	format = '%(sigla)s'
	)