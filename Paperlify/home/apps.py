#Configuration for home app using the AppConfig class
from django.apps import AppConfig


class HomeConfig(AppConfig):
    #Setting default auto-generated field for models in the app
    default_auto_field = 'django.db.models.BigAutoField'
    #Assigning the name of the app
    name = 'home'
