from django.apps import AppConfig


class PublicDataAcquisitionUnitConfig(AppConfig):
    name = 'Public_Data_Acquisition_Unit'

    def ready(self):
        print(f'{self.name} -> Initialized')
        import Public_Data_Acquisition_Unit.sygnals_manager