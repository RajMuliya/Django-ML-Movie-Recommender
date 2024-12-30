from django.core.management.base import BaseCommand
from movie_recommender.models import movie_list

class Command(BaseCommand):
    help = "Deletes all data from the movie_list table."

    def handle(self, *args, **options):
        movie_list.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted all data from movie_list table."))
