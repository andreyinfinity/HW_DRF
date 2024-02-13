from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Команда для первоначального заполнения БД данными из дампа БД"""
    def handle(self, *args, **options):
        call_command('loaddata', 'data.json')
