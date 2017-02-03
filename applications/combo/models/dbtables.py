
TipoGraduacao = db.define_table('tipoGraduacao',
                                Field('tipo', 'string', label = 'Tipo:'),
                                format = '%(tipo)s'
                                )

Graduacao = db.define_table('graduacao',
                            Field('tipoGraduacao', 'reference tipoGraduacao', label='Tipo:',
                            			widget=SQLFORM.widgets.checkboxes.widget, 
                            			requires = IS_IN_DB(db, 'tipoGraduacao.id', '%(tipo)s', 
                            			multiple=True)),
                            Field('cor', 'string', label='Cor:'),
                            Field('grau', 'string', label='Grau:'),                            
                            Field('tempMinimo', 'string', label='Tempo Mínimo:'),
                            )