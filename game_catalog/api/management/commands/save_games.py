from django.core.management.base import BaseCommand
from api.utils.games_dowloader import GamesDownloader


class Command(BaseCommand):
    help = 'Downloading games from igdb api to database'

    def handle(self, *args, **options):
        downloader = GamesDownloader()
        downloader.download()



