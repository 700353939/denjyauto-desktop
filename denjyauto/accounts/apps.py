from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'denjyauto.accounts'

    def ready(self):
        import denjyauto.accounts.signals
