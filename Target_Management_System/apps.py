from django.apps import AppConfig


class TargetManagementSystemConfig(AppConfig):
    name = 'Target_Management_System'

    def ready(self):
        print(f'{self.name} -> initialized')