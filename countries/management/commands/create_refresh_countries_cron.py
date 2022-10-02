from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from countries.tasks import refresh_countries


class Command(BaseCommand):
    def handle(self, *args, **options):

        refresh_countries.delay()

        task_exists = PeriodicTask.objects.filter(
            task="countries.tasks.refresh_countries"
        )

        if not task_exists:

            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.MINUTES,
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name="Refresh Countries",
                task="countries.tasks.refresh_countries",
            )
