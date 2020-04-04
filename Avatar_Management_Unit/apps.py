from django.apps import AppConfig


class AvatarManagementUnitConfig(AppConfig):
    name = 'Avatar_Management_Unit'

    def ready(self):
        print(f'{self.name} -> initialized')