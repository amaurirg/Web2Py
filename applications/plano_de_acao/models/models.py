DEP = db.define_table('departamento',
	Field('setor'),
	format = '%(setor)s'
	)

PROB = db.define_table('problemas',
	Field('problema'),
	format = '%(problema)s'
	)


PLANO = db.define_table('plano',
	Field('depto', 'reference departamento', notnull=True, ondelete='SET NULL', label="Depto"),
	Field('titulo', 'reference problemas', notnull=True, label="Título"),
	Field('descricao', 'text', notnull=True, label="Descrição"),
	Field('plano', 'text', notnull=False, label="Plano"),
	Field('acao', 'text', notnull=False, label="Ação"),
	Field('solucao', 'text', notnull=False, label="Solução"),
	Field('prazo', 'date', notnull=True, label="Prazo"),
	format = '%(titulo)s'
	)

