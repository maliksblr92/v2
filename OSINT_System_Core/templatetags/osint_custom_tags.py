from django import template
register = template.Library()


@register.filter(name='mongoid')
def mongoid(obj, attribute):

    return obj[attribute]['$oid']


@register.filter(name='data_type')
def data_type(obj):

    if(isinstance(obj,(list))):
        return 'list'

    elif(isinstance(obj,dict)):
        return 'dict'

    else:
        return 'var'