from django.core.management.base import BaseCommand
from apps.codificadores.scripts.poblar_codificadores import poblar_codificadores


class Command(BaseCommand):
    help = "Pobla la base de datos con la base de conocimiento proporcionada"

    def handle(self, *args, **options):
        poblar_codificadores()
        self.stdout.write(self.style.SUCCESS("!Base de datos poblada exitosamente!"))
