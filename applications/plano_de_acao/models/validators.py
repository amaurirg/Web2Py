PLANO.depto.requires = IS_IN_DB(db,'departamento.id', '%(setor)s', zero = 'Setor')
PLANO.titulo.requires = IS_IN_DB(db,'problemas.id', '%(problema)s', zero = 'Título')
PLANO.descricao.requires = IS_NOT_EMPTY()
PLANO.prazo.requires = IS_EMPTY_OR(IS_DATE(format=T('%d/%m/%Y'), error_message='O formato deve ser DD/MM/AAAA'))

DEP.setor.requires = IS_NOT_EMPTY()
