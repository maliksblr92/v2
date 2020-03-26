from django.contrib.auth.models import Permission
from django.contrib.contenttypes.views import ContentType

from Target_Management_System.views import Add_Target

content_type = ContentType.objects.get_for_model(Add_Target)
permission = Permission.objects.create(
    codename='can_view_tso_addtarget',
    name='Can View TSO Add Target Page',
    content_type=content_type,
)
