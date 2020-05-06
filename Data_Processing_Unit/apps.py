from django.apps import AppConfig


class DataProcessingUnitConfig(AppConfig):
    name = 'Data_Processing_Unit'

    def ready(self):
        print(f'{self.name} -> initialized')