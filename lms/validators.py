from rest_framework import serializers


class YouTubeOnlyValidator:
    """Валидатор для проверки наличия 'youtube.com/' в поле"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        validation_value = dict(value).get(self.field)
        if validation_value:
            if 'youtube.com/' not in validation_value.lower():
                raise serializers.ValidationError("Можно добавлять ссылки только с Youtube")
        return value
