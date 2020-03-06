from django.conf import settings # import the settings file

def ess_ip(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ESS_IP': settings.ESS_IP}


def uis_ip(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'UIS_IP': settings.UIS_IP}