from django import template
register = template.Library()


@register.filter(name='mongoid')
def mongoid(obj, attribute):

    return obj[attribute]['$oid']

