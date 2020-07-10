"""
management command for creating groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """
    create groups of users
    """

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='tso')
        Group.objects.get_or_create(name='tmo')
        Group.objects.get_or_create(name='rdo')
        Group.objects.get_or_create(name='pao')
