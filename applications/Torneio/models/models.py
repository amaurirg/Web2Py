CLUBES = db.define_table('equipes',
	Field('nome', label='Nome'),
	Field('clube', label='Clube'),
	Field('pontos', label='Pontos'),
	Field('jogos', label='Jogos'),
	Field('vitorias', label='Vitórias'),
	Field('empates', label='Empates'),
	Field('derrotas', label='Derrotas'),
	Field('gols_pro', label='Gols Pró'),
	Field('gols_contra', label='Gols Contra'),
	Field('saldo_gols', label='Saldo de Gols')
	)

