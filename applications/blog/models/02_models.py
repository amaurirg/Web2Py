# -*-coding: utf-8 -*-

# categories
Categories = db.define_table('categories',
	Field('name', length=256, notnull=True, label='Nome'),
	format = '%(name)s'
	)

# posts
Posts = db.define_table('posts',
	Field('title', length=256, notnull=True, label='Título'),
	Field('body', 'text', notnull=True, label='Conteúdo'),
	Field('image_cover', 'upload', label='Imagem da Capa'),
	Field('category', 'reference categories', ondelete='SET NULL', label='Categoria'),
	Field('likes', 'integer', default=0, label='Curtidas'),
	auth.signature,
	format = '%(title)s'
	)

# comments
Comments = db.define_table('comments',
	Field('body', 'text', notnull=True, label='Mensagem'),
	Field('post', 'reference posts', notnull=True, label='Postagem'),
	auth.signature
	)