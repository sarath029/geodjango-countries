from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    def handle(self, *args, **options):

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name="Refresh Countries",
            task="countries.tasks.refresh_countries",
        )
