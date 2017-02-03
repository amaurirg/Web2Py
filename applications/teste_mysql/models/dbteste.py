PESSOAS = db.define_table('pessoas',
	Field('nome', notnull=True),
	Field('sexo', requires=IS_IN_SET(['M', 'F'], zero='Sexo'))
	)
