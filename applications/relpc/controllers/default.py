# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import platform, os


def index():
    if not os.path.exists('C:\\temprel'):
        os.makedirs("c:\\temprel")

    if platform.release() == "XP":
        os.system("WMIC /output:C:\\temprel\pro.txt product get name, version, installdate")
    else:
        os.system("Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, InstallDate | Sort-Object -Property DisplayName -Unique | Format-Table -AutoSize > c:\\temprel\pro.txt")


    with open("C:\\temprel\\pro.txt") as f:
            file = f.read()

    message = """
    Nome do computador: {0}
    Sistema: {1}
    Versão: {2}
    Plataforma: {3}
    Máquina: {4}
    Arquitetura: {5}
    Processador: {6}\n
    Programas Instalados: \n{7}
    """.format(
    platform.node(),
    platform.system(),
    platform.release(),
    platform.platform(),
    platform.machine(),
    platform.architecture(),
    platform.processor(),
    file)

    if not os.path.exists('C:\\relpc'):
        os.makedirs("c:\\relpc")
    with open("c:\\relpc\\relatorio.txt", "w") as w:
        w.write(message)

    return "OK"

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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


