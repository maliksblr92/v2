from django.apps import AppConfig


class KeybaseManagementSystemConfig(AppConfig):
    name = 'Keybase_Management_System'

    def ready(self):
        print(f'{self.name} -> initialized')