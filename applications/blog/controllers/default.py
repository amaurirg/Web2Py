# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*5
    end = page*5
    posts = db(Posts).select(orderby=Posts.created_on, limitby=(start, end))

    categories = db(Categories).select(limitby=(0,10))
    return dict(posts=posts, categories=categories)
    
def teste_de_view():
    return dict()

def teste_de_view2():
    button = A('Botão', _href='#', _class='btn btn-success')
    form = FORM(INPUT(_type='text'), INPUT(_type='submit'))
    return dict(button=button, form=form)


def categories():
    grid = SQLFORM.grid(Categories)
    return dict(grid=grid)

##@auth.requires_permission('create')
def new_category():
    form = SQLFORM(Categories)
    if form.process().accepted:
        response.flash = 'Nova categoria criada!'
        redirect (URL('categories'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'
    return dict(form=form)


def update_category():
    category = db(Categories.id == request.args(0, cast=int)).select().first()
    form = SQLFORM(Categories, category)
    if form.process().accepted:
        response.flash = 'Você editou o registro!'
        redirect(URL('categories'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Nenhuma alteração foi realizada!'
    return dict(form=form,category=category)

def delete_category():
    db(Categories.id == request.args(0,cast = int)).delete()
    return dict()

def post():
    post = db(Posts.id == request.args(0,cast=int)).select().first()
    comments = db(Comments.post == post.id).select()
    Comments.post.default = post.id
    form = SQLFORM(Comments, formstyle='divs',submit_button='Enviar')
    if form.process().accepted:
        redirect(URL('post',args=post.id))
    button = A('like',_href=URL('like', args=post.id),_class='btn')

    return dict(post=post, comments=comments, form=form, button=button)

def like():
    post = db(Posts.id == request.args(0,cast=int,)).select().first()
    if not session.liked:
        session.liked = {'like':None,'post':None}
    if not session.liked['like'] or session.liked['post'] != post.id:
        post.update_record(likes=post.likes+1)
        db.commit()
        session.liked = {'like':True, 'post':post.id}
    else:
        session.flash = 'Você já curtiu este post.'

    redirect(URL('post', args=post.id))


def posts():
    grid = SQLFORM.grid(Posts)
    return dict(grid=grid)

@auth.requires_membership('admin')
def new_post():
    form = SQLFORM(Posts)
    if form.process().accepted:
        response.flash = 'Formulário aceito!'
    elif form.errors:
        response.flash = "Erros no formulário!"
    else:
        response.flash = "Preencha o formulário!"
    return dict(form = form)

def edit_post():
    form = crud.update(Posts, request.args(0, cast=int))
    return dict(form=form)    

@auth.requires_login()
def delete_post():
    db(Posts.id == request.args(0, cast=int)).delete()
    redirect(URL('index'))

def delete_comment():
    db(Comments.id == request.args(0, cast=int)).delete()
    redirect(URL('index'))

def search():
    posts = None
    form = SQLFORM.factory(
Field('keyword', label='Palavra-chave')
    )
    if form.process().accepted:
        posts = db(Posts.title.like('%'+form.vars.keyword+'%')).select()
    return dict(form=form, posts=posts)

def search2():
    search = request.vars.search or ''
    posts = db(Posts.title.like('%'+search+'%')).select(orderby=Posts.created_on)
    return dict(posts=posts)

def contact():
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY(), label='Nome'),
        Field('email', requires=IS_EMAIL(), label="Email"),
        Field('message', 'text', requires=IS_NOT_EMPTY(), label='Mensagem'),
        formstyle='divs',
        submit_button='Enviar'
        )
    ##button = A('Home', _href='{{=URL('index.html')}}', _class='btn btn-success')
    if form.process().accepted:
        mail.send(to=form.vars.email,
            subject='Contato no Blog',
            reply_to=form.vars.email,
            message='Nova mensagem no blog: %(mensagem)s'%{'mensagem':form.vars.message}
            )
        response.flash = 'Email enviado com sucesso!'

    return dict(form=form)

def contact_html():
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY(), label='Nome'),
        Field('email', requires=IS_EMAIL(), label="Email"),
        Field('message', 'text', requires=IS_NOT_EMPTY(), label='Mensagem'),
        formstyle='divs',
        submit_button='Enviar'
        )
    
    if form.process().accepted:
        mail.send(to=form.vars.email,
            subject='Contato no Blog',
            reply_to=form.vars.email,
            message="""<html>
            <strong>Novo contato no blog</strong><br>
            %(name)s enviou a seguinte mensagem: <br>
            %(message)s
            </html>"""%{'name':form.vars.name, 'message':form.vars.message},
            ##attachments = [mail.attachment('path/to/file')]
            )
        response.flash = 'Email enviado com sucesso!'
    return dict(form=form)

def admin():
    response.view = 'layout_admin.html'
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

    form = auth()
    return dict(form=form)

def user_false():
    form = auth.register()
    return dict(form=form)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
