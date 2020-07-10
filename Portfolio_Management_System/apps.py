from django.apps import AppConfig


class PortfolioManagementSystemConfig(AppConfig):
    name = 'Portfolio_Management_System'

    def ready(self):
        print(f'{self.name} -> initialized')