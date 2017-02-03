"""
   web2py widgets
   A collection of user interface widgets for web2py
   Developed by Nathan Freeze
   Copyright 2010 nathan@freezable.com
   License: GPLv2
"""

import uuid
import datetime

#Script resource URLs
star_rating_js = URL(r=request,c='static/stars',f='jquery.ui.stars.js')
multi_select_js = URL(r=request,c='static/multiselect',f='jquery.multiSelect.js')
jq_ui = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.js'

#CSS resource URLs
star_rating_css = URL(r=request,c='static/stars',f='jquery.ui.stars.css')
multi_select_css = URL(r=request,c='static/multiselect',f='jquery.multiSelect.css')
ui_base_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/base/jquery-ui.css'
ui_darkness_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/ui-darkness/jquery-ui.css'
ui_blacktie_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/black-tie/jquery-ui.css'
ui_blitzer_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/blitzer/jquery-ui.css'
ui_cupertino_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/cupertino/jquery-ui.css'
ui_darkhive_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/dark-hive/jquery-ui.css'
ui_dotlove_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/dot-luv/jquery-ui.css'
ui_eggplant_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/eggplant/jquery-ui.css'
ui_excitebike_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/excite-bike/jquery-ui.css'
ui_flick_theme = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/themes/flick/jquery-ui.css'

#Default jQueryUI theme
default_theme = ui_darkness_theme

class UISliderWidget(object):
    """
       Represent a numeric value using the jQueryUI slider  
       based on http://jqueryui.com/demos/slider/     
    """
    def __init__(self, ui_js = jq_ui, 
                       ui_css = default_theme, 
                       width=200,
                       min = 0, max = 100, step = 1, 
                       orientation = 'horizontal',
                       animate = True,
                       disabled = False):
        if not ui_js in response.files:
            response.files.append(ui_js)
        if not ui_css in response.files:
            response.files.append(ui_css)
        self.width = width
        self.min = min
        self.max = max
        self.step = step
        self.orientation = orientation
        self.animate = animate
        self.disabled = disabled
    def widget(self, f, v):
        uid = str(uuid.uuid4())[:8]
        opts = 'min: %s, max: %s, step: %s, orientation: "%s", animate: %s, disabled: %s' % \
                (self.min, self.max, self.step, self.orientation, 
                 str(self.animate).lower(),str(self.disabled).lower())
        wrapper = DIV(_id="slider_wrapper_%s" % uid,
                      _style="width: %spx;text-align:center;" % self.width)
        inp = SQLFORM.widgets.string.widget(f,v)
        sld = DIV(_id='slider_' + inp['_id'] + '_%s' % uid)
        sldval = SPAN(inp['_value'],_id=sld['_id']+'_val')
        scr1 = "jQuery('#%s').hide();" % inp['_id']
        scr2 = "jQuery('#%s').val(ui.value);jQuery('#%s').text(ui.value);" % (inp['_id'], sldval['_id'])
        jqscr = SCRIPT(scr1,"jQuery('#%s').slider({value: %s, stop: function(event, ui) {%s}, %s});" % \
                        (sld['_id'], inp['_value'],scr2, opts),_type="text/javascript")
        wrapper.components.extend([sld,sldval,inp,jqscr])
        return wrapper
    
class UIDatePickerWidget(object):
    """
       Enable date input using the jQueryUI date picker widget
       based on http://jqueryui.com/demos/datepicker/
    """
    def __init__(self, ui_js = jq_ui, 
                       ui_css = default_theme,
                       format = 'yy-mm-dd'):
        if not ui_js in response.files:
            response.files.append(ui_js)
        if not ui_css in response.files:
            response.files.append(ui_css)
        self.format = format
    def widget(self, f, v):        
        wrapper = DIV()
        inp = SQLFORM.widgets.string.widget(f,v,_class="jqdate")
        jqscr = SCRIPT("jQuery(document).ready(function(){"\
                       "jQuery('#%s').datepicker({dateFormat:'%s'});});" % \
                         (inp['_id'], self.format),_type="text/javascript")
        wrapper.components.extend([inp,jqscr])
        return wrapper
    
class UIAutocompleteWidget(object):
    """
      An autocomplete widget using jQueryUI  
    """
    def __init__(self, ui_js = jq_ui, 
                       ui_css = default_theme,
                       min_length = 2, 
                       delay = 300,
                       disabled = False, 
                       url = None):
        if not ui_js in response.files:
            response.files.append(ui_js)
        if not ui_css in response.files:
            response.files.append(ui_css)
        self.min_length = min_length
        self.delay = delay
        self.disabled = disabled
        self.url = url        
    def widget(self, f, v):
        d_id = "autocomplete-" + str(uuid.uuid4())[:8]
        wrapper = DIV(_id=d_id)
        inp = SQLFORM.widgets.string.widget(f,v)
        opts = 'minLength: %s, delay: %s, disabled: %s' % \
               (self.min_length,self.delay,str(self.disabled).lower()) 
        if self.url: 
            scr = SCRIPT('jQuery("#%s input").autocomplete({source: "%s", %s});' % \
                  (d_id, self.url, opts))
        else:
            rows = f._db(f._table['id']>0).select(f,distinct=True)
            itms = [str(t[f.name]) for t in rows]
            scr = SCRIPT('var data = "%s".split("|");'\
                         'jQuery("#%s input").autocomplete({source: data, %s});' % \
                              ("|".join(itms),d_id,opts))
        wrapper.append(inp)
        wrapper.append(scr)
        return wrapper

class CascadingSelect(object):
    """
       Creates dependent selects based on table relationships.
       Pass the tables in order of least to most specific
       Based on http://web2pyslices.com/main/slices/take_slice/85
    """
    def __init__(self, *tables):
        self.tables = tables 
        self.prompt = lambda table:str(table)   
    def widget(self,f,v):
        uid = str(uuid.uuid4())[:8]
        d_id = "cascade-" + uid
        wrapper = TABLE(_id=d_id)
        parent = None; parent_format = None; 
        fn =  '' 
        vr = 'var dd%s = [];var oi%s = [];\n' % (uid,uid)
        prompt = [self.prompt(table) for table in self.tables]
        vr += 'var pr%s = ["' % uid + '","'.join([str(p) for p in prompt]) + '"];\n' 
        f_inp = SQLFORM.widgets.string.widget(f,v)
        f_id = f_inp['_id']
        f_inp['_type'] = "hidden"
        for tc, table in enumerate(self.tables):             
            db = table._db     
            format = table._format            
            options = db(table['id']>0).select()
            id = str(table) + '_' + format[2:-2]             
            opts = [OPTION(format % opt,_value=opt.id,
                                 _parent=opt[str(parent)] if parent else '0') \
                                  for opt in options]
            opts.insert(0, OPTION(prompt[tc],_value=0))
            inp = SELECT(opts ,_parent=str(parent) + \
                                  "_" + str(parent_format),
                                  _id=id,_name=id,
                                  _disabled="disabled" if parent else None)
            wrapper.append(TR(inp))
            next = str(tc + 1)
            vr += 'var p%s = jQuery("#%s #%s"); dd%s.push(p%s);\n' % (tc,d_id,id,uid,tc)            
            vr += 'var i%s = jQuery("option",p%s).clone(); oi%s.push(i%s);\n' % (tc,tc,uid,tc)
            fn_in = 'for (i=%s;i<%s;i+=1){dd%s[i].find("option").remove();'\
                    'dd%s[i].append(\'<option value="0">\' + pr%s[i] + \'</option>\');'\
                    'dd%s[i].attr("disabled","disabled");}\n' % \
                           (next,len(self.tables),uid,uid,uid,uid)
            fn_in +='oi%s[%s].each(function(i){'\
                    'if (jQuery(this).attr("parent") == dd%s[%s].val()){'\
                    'dd%s[%s].append(this);}});' % (uid,next,uid,tc,uid,next)            
            fn_in += 'dd%s[%s].removeAttr("disabled");\n' % (uid,next)
            fn_in += 'jQuery("#%s").val("");' % f_id
            if (tc < len(self.tables)-1):
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in) 
            else:
                fn_in = 'jQuery("#%s").val(jQuery(this).val());' % f_id
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in)
                if v:
                    fn += 'dd%s[%s].val(%s);' % (uid,tc,v)                       
            parent = table
            parent_format = format[2:-2]

        wrapper.append(f_inp)
        wrapper.append(SCRIPT(vr,fn))
        return wrapper
    
class MultiSelectWidget(object):
    """
       A web2py multi-select widget based on this jQuery plugin:
       http://abeautifulsite.net/2008/04/jquery-multiselect/
       Download the plugin and extract to a folder called
        'multiselect' in your static folder.
       Pass the urls of the plugin javascript and css to __init__
       Based on http://web2pyslices.com/main/slices/take_slice/70
    """
    def __init__(self, js = multi_select_js, 
                       css = multi_select_css):
        if not js in response.files:
            response.files.append(js)
        if not css in response.files:
            response.files.append(css)
    def widget(self, f, v):       
        d_id = "multiselect-" + str(uuid.uuid4())[:8]
        wrapper = DIV(_id=d_id)
        inp = SQLFORM.widgets.options.widget(f,v)
        inp['_multiple'] = 'multiple'
        inp['_style'] = 'min-width: %spx;' % (len(f.name) * 20 + 50)
        if v:
            if not isinstance(v,list): v = str(v).split('|')
            opts = inp.elements('option')
            for op in opts:
                if op['_value'] in v:
                    op['_selected'] = 'selected'            
        scr = SCRIPT('jQuery("#%s select").multiSelect({'\
                     'noneSelected:"Select %ss"});' % (d_id,f.name))
        wrapper.append(inp)
        wrapper.append(scr)
        if request.vars.get(inp['_id']+'[]',None):
            var = request.vars[inp['_id']+'[]']
            if not isinstance(var,list): var = [var]
            request.vars[f.name] = '|'.join(var)
            del request.vars[inp['_id']+'[]']
        return wrapper    
  
class DropdownDateWidget():
    """
       A date selector that uses html select inputs
       Based on http://web2pyslices.com/main/slices/take_slice/25
    """
    def __init__(self, days = None, 
                 months = None, years = None):
        if not days:
            days = [OPTION(str(i).zfill(2)) for i in range(1,32)]
        self.days = days
        if not months:
            months = [OPTION(datetime.date(2008,i,1).strftime('%B')
                        ,_value=str(i).zfill(2)) for i in range(1,13)]
        self.months = months
        if not years:            
            years = [OPTION(i) for i in range(request.now.year-50,
                                              request.now.year+50)]
        self.years = years
    def widget(self, f, v):
        dtval = v if v else request.now.isoformat()
        y,m,d= str(dtval).split("-") 
        dt = SQLFORM.widgets.string.widget(f,v)
        uid = str(uuid.uuid4())[:8]
        dayid = dt['_id'] + '_day_' + uid
        monthid = dt['_id'] + '_month_' + uid
        yearid = dt['_id'] + '_year_' + uid
        wrapper = DIV(_id=dt['_id']+"_wrapper_" + uid)
        day = SELECT(self.days, value=d,_id=dayid)
        month = SELECT(self.months, value=m,_id=monthid)
        year = SELECT(self.years,
                     value=y,_id=yearid)
        setval = "var curval = jQuery('#%s').val();if(curval){var pcs = curval.split('-');"\
                 "var dd = pcs[2];var mm = pcs[1];var yy = pcs[0];"\
                 "jQuery('#%s').val(dd);jQuery('#%s').val(mm);jQuery('#%s').val(yy);}" % \
                                  (dt['_id'], dayid , monthid, yearid)
        combined = "jQuery('#%s').val()+'-'+jQuery('#%s').val()+'-'+jQuery('#%s').val()" % \
                                          (yearid, monthid, dayid)
        combine = "jQuery('#%s').val(%s);" % (dt['_id'],combined)
        onchange = "jQuery('#%s select').change(function(e){%s});" % \
                                             (wrapper['_id'], combine)
        jqscr = SCRIPT("jQuery('#%s').hide();%s%s" % (dt['_id'],setval,onchange))
        wrapper.components.extend([month,day,year,dt,jqscr])
        return wrapper    

class InplaceEditWidget(object):
    def __init__(self):
        pass
    def widget(self, f, v):
        wrapper = DIV()
        inp = SQLFORM.widgets.string.widget(f,v)
        lbl = SPAN(inp['_value'],_id='inplace_edit_'+inp['_id'],_style="cursor:pointer;")
        scr1 = "jQuery('#%s').hide();" % inp['_id']
        scr2 = "jQuery('#%s').bind('dblclick',function(e){ jQuery(this).hide();jQuery('#%s').show().focus();});" % \
                             (lbl['_id'],inp['_id'])
        scr3 = "jQuery('#%s').bind('blur',function(e){ jQuery(this).hide();jQuery('#%s').show().text(jQuery(this).val());});" % \
                             (inp['_id'],lbl['_id'])
        jqscr = SCRIPT(scr1,scr2,scr3,_type="text/javascript")
        wrapper.components.extend([inp,lbl,jqscr])
        return wrapper
    
class StarRatingWidget(object):
    """
       Allows integer input using a star rating
       Download the jQuery plugin from:
       http://orkans-tmp.22web.net/star_rating/index.html
       Extract to a folder named 'stars' in your static folder
    """
    def __init__(self, ui_js = jq_ui, 
                       stars_js = star_rating_js, 
                       stars_css = star_rating_css,
                       single_vote = False,
                       disabled = False):
        if not ui_js in response.files:
            response.files.append(ui_js)
        if not stars_js in response.files:
            response.files.append(stars_js)
        if not stars_css in response.files:
            response.files.append(stars_css)
        self.disabled = disabled
        self.single_vote = single_vote
    def widget(self, f, v):
        uid = str(uuid.uuid4())[:8]
        opts = 'disabled: %s, oneVoteOnly: %s' % (str(self.disabled).lower(),
                                                  str(self.single_vote).lower())
        wrapper = DIV(SPAN(_id="stars-cap"),
                      _id="stars-wrapper_%s" % uid)
        from gluon.sqlhtml import OptionsWidget
        inp = OptionsWidget.widget(f,v)
        scr = SCRIPT('jQuery("#stars-wrapper_%s").stars('\
                     '{inputType: "select", %s});' % (uid, opts))
        wrapper.append(inp)
        wrapper.append(scr)
        return wrapper
       
