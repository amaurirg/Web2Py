def filtra():
	# planos = db(PLANO).select(orderby=db.plano.x)
	print 'função'
	# print request.vars
	return 'retornou'


def concluidos():
	planos = db(PLANO.concluido == 'NÃO').select(orderby=db.plano.prazo)
	print planos
	return planos