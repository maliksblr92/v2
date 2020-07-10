from django.apps import AppConfig


class UserAccountsManagementUnitConfig(AppConfig):
    name = 'User_Accounts_Management_Unit'

    def ready(self):
        print(f'{self.name} -> initialized')