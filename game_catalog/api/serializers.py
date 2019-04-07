from api.models import Game, Must, Image, Platform, Genre
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',)


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'images')


class GameDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'release_date', 'users_rating', 'users_views', 'images', 'platforms',
                  'genres')


class MustSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Must
        fields = ('owner', 'game', 'count')





