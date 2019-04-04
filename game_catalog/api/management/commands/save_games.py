from django.core.management.base import BaseCommand
from api.tasks import save_games


class Command(BaseCommand):
    help = 'Downloading games from igdb api to database'

    def handle(self, *args, **options):
        save_games.delay()



