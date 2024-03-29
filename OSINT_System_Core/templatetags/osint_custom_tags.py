from django import template
register = template.Library()


@register.filter(name='mongoid')
def mongoid(obj, attribute):

    return obj[attribute]['$oid']


@register.filter(name='encode_url')
def encode_url(obj):
    print('encoding url')


    return obj.replace('/',' ')

@register.filter(name='get_vedio_id')
def get_vedio_id(url):
    print('encoding url')


    return url.split('=')[1]


@register.filter(name='data_type')
def data_type(obj):

    if(isinstance(obj,(list))):
        return 'list'

    elif(isinstance(obj,dict)):
        return 'dict'

    else:
        return 'var'

#ahmed code 
@register.filter(name='data_type')
def split(obj):

    if(isinstance(obj,(list))):
        return 'list'

    elif(isinstance(obj,dict)):
        return 'dict'

    else:
        return 'var'
    
@register.filter(name='to_and')
def to_and(value):
    arr=value.split('/')
    new_value=arr[2]+"-"+arr[0]+"-"+arr[1]
  
    return new_value

@register.filter(name='img_count')
def img_count(value):
    length=len(value)
   
    return length

@register.filter(name='split_latlons')
def split_latlons(latlons):

    return latlons.replace(',','_')

# ahmed
@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se este usuário pertence a um grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False