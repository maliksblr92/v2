from django.apps import AppConfig


class CaseManagementSystemConfig(AppConfig):
    name = 'Case_Management_System'

    def ready(self):
        print(f'{self.name} -> initialized')