from django.conf import settings as django_settings

class SettingsHandler(object):
    
    def __init__(self, app_settings):
        self.app_settings = app_settings
    
    def __getattr__(self, attr):
        try:
            return getattr(django_settings, attr)
        except AttributeError:
            return getattr(self.app_settings, attr)
