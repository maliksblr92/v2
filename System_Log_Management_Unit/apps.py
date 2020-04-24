from django.apps import AppConfig


class SystemLogManagementUnitConfig(AppConfig):
    name = 'System_Log_Management_Unit'

    def ready(self):
        print(f'{self.name} -> initialized')