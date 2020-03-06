from django.apps import AppConfig


class PublicDataAcquisitionUnitConfig(AppConfig):
    name = 'Public_Data_Acquisition_Unit'

    def ready(self):
        print('....................{0}...Initiated................................'.format(self.name))
        import Public_Data_Acquisition_Unit.sygnals_manager