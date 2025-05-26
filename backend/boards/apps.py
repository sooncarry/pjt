from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.management import call_command
from django.db.models.signals import post_migrate

class BoardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boards'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    try:
        from .models import Post
        if not Post.objects.exists():
            call_command('loaddata', 'board_data.json', verbosity=0)
    except (OperationalError, ProgrammingError):
        pass
