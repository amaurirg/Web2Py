# =*= coding: utf-8 -*-

#Ramais
NR = db.define_table('nome_ramal',
	Field('nome', notnull=True, label="Nome"),
	Field('ramal', notnull=True, label="Ramal"),
	Field('depto', notnull=True, label="Departamento"),
	Field('email', notnull=True, label="Email"),
	format = '%(nome)s - %(ramal)s'
	)
db.nome_ramal.depto.widget = SQLFORM.widgets.autocomplete(request, db.nome_ramal.depto, limitby=(0,1), min_length=1)

TIPO = db.define_table('lista_status',
	Field('tipo_status'),
	format = '%(tipo_status)s'
	)

CONF = db.define_table('env_email',
	Field('sel', notnull=False),
	format = '%(sel)s'
	)
#Recepção
REC = db.define_table('recepcao',
	Field('nome', notnull=True, label='Nome'), 
	Field('tel', notnull=True, label='Telefone'),
	Field('emp', notnull=False, label='Empresa'),
	Field('ramal', 'reference nome_ramal', ondelete='SET NULL', label='Ramal Solicitado'),
	Field('prod', notnull=False, label='Produto'),
	Field('status', 'reference lista_status', ondelete='SET NULL', label='Status'),
	Field('obs', 'text', notnull=False, label='Observações'),
	Field('msg', 'text', notnull=False, label ='Mensagem'),
	Field('env', 'reference env_email', ondelete='SET NULL', label='Enviar email?'),
	# auth.signature,
	format = '%(nome)s'
	)
#db.recepcao.env.widget = SQLFORM.widgets.date.widget