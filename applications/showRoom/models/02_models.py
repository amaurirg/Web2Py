# =*= coding: utf-8 -*-

#Cameras
CAM = db.define_table('cameras',
	Field('foto', 'upload'),
	Field('fabricante', default='-', notnull=True, label="FABRICANTE"),
	Field('modelo', default='-', notnull=True, label="MODELO"),
	Field('tipo', default='-', notnull=True, label="TIPO"),
	Field('tec', default='-', notnull=True, label="TECNOLOGIA"),
	Field('lente', default='-', notnull=True, label="LENTE"),
	Field('angulo', default='-', notnull=True, label="ÂNGULO DE VISÃO"),
	Field('resolucao', default='-', notnull=True, label="RESOLUÇÃO"),
	Field('wdr_blc', default='-', notnull=True, label="WDR/BLC"),
	Field('alcance_ir', default='-', notnull=True, label="ALCANCE DO IR"),
	Field('consumo', default='-', notnull=True, label="CONSUMO MÁXIMO"),
	Field('grau', default='-', notnull=True, label="GRAU DE PROTEÇÃO"),
	Field('int_ext', default='-', notnull=True, label="LOCAL DE INSTALAÇÃO"),
	Field('ip', default='-', notnull=True, label="IP"),
	Field('onvif', default='-', notnull=True, label="ONVIF"),
	Field('usuario', default='-', notnull=True, label="USUÁRIO"),
	Field('senha', default='-', notnull=True, label="SENHA"),
	Field('serial', default='-', notnull=True, label="SERIAL"),
	Field('switch_poe', default='-', notnull=True, label="SWITCH POE"),
	# auth.signature,
	format = '%(fabricante)s - %(modelo)s'
	)
#db.nome_ramal.depto.widget = SQLFORM.widgets.autocomplete(request, db.nome_ramal.depto, limitby=(0,1), min_length=1)

def imprime(x):
	print(x)


def busca():
    camera = '' 
    if not request.vars.page:
        redirect(URL(vars={'camera':request.vars.camera, 'page':1}))
    else:
        page =int(request.vars.page)
    start = (page-1)*5
    end = page*5
    if request.vars.camera:
        camera = db(CAM.fabricante.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end)) | db(CAM.modelo.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end))  | db(CAM.tipo.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end)) | db(CAM.lente.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end)) | db(CAM.resolucao.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end)) | db(CAM.alcance_ir.like('%'+request.vars.camera+'%')).select(orderby=CAM.fabricante, limitby=(start,end))
        if len(camera)==1:
            lbl = H3('Câmera Selecionada', _class='test', _id=0)
        else:
            lbl = H3('Câmeras Selecionadas', _class='test', _id=0)
        lbl2 = ''
    else:
        lbl = H3('Nenhuma Câmera Selecionada', _class='test', _id=0)
        lbl2 = H4('Digite em buscar para selecionar ou clique em Câmeras para visualizar a lista geral', _class='test', _id=0)
    return camera, lbl, lbl2

