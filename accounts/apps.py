from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Import signals module

#class DashboardConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    #name = 'dashboard'

    #def ready(self):
        #import dashboard.signals  # Import signals module
