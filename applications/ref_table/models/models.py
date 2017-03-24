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
	Field('usuario'),
	# Field('usuario',db.auth_user, default=auth.user_id if auth.is_logged_in() ele None),
	# Field('data', 'date', default=request.now )  
	auth.signature
	)


# signature = db.Table(db, 'signature',
#     Field('created_on', 'datetime', default=request.now),
#     Field('created_by', db.auth_user, default=auth.user_id),
#     Field('updated_on', 'datetime', default=request.now),
#     Field('updated_by', db.auth_user, update=auth.user_id))
# db.define_table('payment', signature, Field('amount', 'double'))