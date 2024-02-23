from rest_framework import serializers


class YouTubeOnlyValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com/' not in dict(value).get(self.field).lower():
            raise serializers.ValidationError("Можно добавлять ссылки только с Youtube")
        return value
