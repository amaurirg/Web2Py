def atualiza_pontos():
	# equipe = request.vars.
	dados = db(CLUBES.clube=="Palmeiras").select()
	print request.vars
	# print request.vars.name
	grid = SQLFORM.grid(CLUBES)
	return grid
	# print dados
	# return 







"""
def index():
    dados = db(CLUBES.clube=="Palmeiras").select(CLUBES.pontos)
    for dado in dados:
        res = int(dado.pontos)
    return res + 3
"""

