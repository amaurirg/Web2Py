# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    links = []
    links.append(A('jQueryUI Slider',_href=URL(r=request,f=slider)))
    links.append(A('jQueryUI Date Picker',_href=URL(r=request,f=datepicker)))
    links.append(A('Autocomplete with local items',_href=URL(r=request,f=autocomplete_local)))
    links.append(A('Autocomplete with remote items',_href=URL(r=request,f=autocomplete_local)))
    links.append(A('Cascading select',_href=URL(r=request,f=cascading_select)))
    links.append(A('Multi-select select',_href=URL(r=request,f=multi_select)))
    links.append(A('Dropdown date picker',_href=URL(r=request,f=dropdown_date)))
    links.append(A('Inplace edit',_href=URL(r=request,f=inplace_edit)))
    links.append(A('Star rating',_href=URL(r=request,f=star_rating)))
    return dict(widgets=links)

def slider():
    slider = UISliderWidget(min=100, max=200, step=2,
                            orientation='vertical')
    db.things.value.widget = slider.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def datepicker():
    datepicker = UIDatePickerWidget(format = 'dd-mm-yy')
    db.things.created_on.widget = datepicker.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def autocomplete_local():
    autocomplete = UIAutocompleteWidget()
    db.things.name.widget = autocomplete.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def autocomplete_remote():
    callback = URL(r=request,f='get_items',
                   vars=dict(table='things',field='name'),
                   extension = 'json')
    autocomplete = UIAutocompleteWidget(url=callback)
    db.things.name.widget = autocomplete.widget
    form = SQLFORM(db.things)
    return dict(form=form)   

def get_items():
    term = request.vars.term
    table = request.vars.table
    field = request.vars.field
    if term and table and field:
        matches = db(db[table][field].like('%'+term+'%')).select()
        for match in matches:
            match.value = match.name        
        return dict(matches=matches.as_list())
    
def cascading_select():
    cascade = CascadingSelect(db.state,db.city,db.zipcode)
    db.things.location.widget = cascade.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def multi_select():
    multi = MultiSelectWidget()
    db.things.stuff.widget = multi.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def dropdown_date():
    dropdown = DropdownDateWidget()
    db.things.created_on.widget = dropdown.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def inplace_edit():
    inplace = InplaceEditWidget()
    db.things.value.widget = inplace.widget
    form = SQLFORM(db.things)
    return dict(form=form)

def star_rating():
    stars = StarRatingWidget(single_vote=True)
    db.things.rating.widget = stars.widget
    form = SQLFORM(db.things)
    return dict(form=form)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


