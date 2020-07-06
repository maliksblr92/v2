from rest_framework import serializers
from OSINT_System_Core.models import Supported_Socail_Sites


class Supported_Socail_Sites_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supported_Socail_Sites
        fields = ('title','website_type','base_url','website_status','health_status','created_by')