from api.utils.games_downloader import GamesDownloader
from game_catalog.celery import app


@app.task
def save_games():
    downloader = GamesDownloader()
    downloader.download()





