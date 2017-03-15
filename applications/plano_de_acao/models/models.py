DEP = db.define_table('departamento',
	Field('setor'),
	format = '%(setor)s'
	)

PROB = db.define_table('problemas',
	Field('problema'),
	format = '%(problema)s'
	)


PLANO = db.define_table('plano',
	Field('depto', 'reference departamento', notnull=True, ondelete='SET NULL', label="Setor"),
	Field('titulo', 'reference problemas', notnull=True, label="Título"),
	Field('descricao', 'text', notnull=True, label="Descrição"),
	Field('plano', 'text', notnull=False, label="Plano"),
	Field('acao', 'text', notnull=False, label="Ação"),
	Field('prazo', 'date', notnull=True, default=datetime.date.today(), label="Prazo"),
	Field('concluido', label='Concluído', widget=SQLFORM.widgets.radio.widget, 
           requires = IS_IN_SET(['NÃO', 'SIM']), default='NÃO'),
	auth.signature,
	format = '%(titulo)s'
	)


STATEND = db.define_table('status_atend',
	Field('status'),
	format = '%(status)s'
	)


ATEND = db.define_table('atendimentos',
	# Field('data_atend', 'date', notnull=True, default=datetime.date.today(), label="Data"),
	Field('cliente', notnull=True, label="Cliente"),
	Field('contato', notnull=True, label="Contato"),
	Field('detalhes', notnull=True, label="Detalhes do Atendimento"),
	Field('status', 'reference status_atend', notnull=True, label="Status"),
	auth.signature,
	format = '%(cliente)s'
	)



response.logo = A(IMG(_src=URL('static', 'images/logoSiteBest.png'), _href=URL('default', 'index')))