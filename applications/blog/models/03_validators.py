# -*- coding: utf-8 -*-

# categories
db.categories.name.requires = IS_NOT_EMPTY(error_message = 'Este campo é obrigatório.')

# posts
Posts.title.requires = IS_NOT_EMPTY()
Posts.body.requires = IS_NOT_EMPTY()
Posts.image_cover.requires = IS_EMPTY_OR(IS_IMAGE())
Posts.category.requires = IS_IN_DB(db,'categories.id', '%(name)s')
Posts.likes.readable = Posts.likes.writable = False

#comments
Comments.body.requires = IS_NOT_EMPTY()
Comments.post.requires = IS_IN_DB(db, 'posts.id', '%(title)s')
Comments.post.readable = Comments.post.writable = False


