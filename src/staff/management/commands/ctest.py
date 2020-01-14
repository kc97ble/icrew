import requests
from django.core.management.base import BaseCommand, CommandError

from events.models import Event
from staff.logics import all_inconsistent_event_ids

TSV_LINK = "https://docs.google.com/spreadsheets/d/1kJHQVorZv4iGmaNtr0Xlf6JwOqiU_MAQOD1noJRMEyU/export?format=tsv"


class Command(BaseCommand):
    help = "Fetch the official schedule and find inconsistencies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--save",
            action="store_true",
            help="Mark inconsistent events with is_inconsistent = True",
        )

    def handle(self, *args, **kwargs):
        response = requests.get(TSV_LINK)
        data = response.content.decode("utf-8")
        if response.status_code == 200:
            ie_ids = all_inconsistent_event_ids(data)
            if ie_ids:
                self.stdout.write(", ".join(map(str, [id for id in ie_ids])))
                self.stdout.write(
                    self.style.WARNING("{} inconsistencies found".format(len(ie_ids)))
                )
            else:
                self.stdout.write(self.style.SUCCESS("No inconsistencies found"))

            if kwargs["save"]:
                events = Event.objects.all()
                for e in events:
                    e.is_inconsistent = e.id in ie_ids
                    e.save()
            elif ie_ids:
                self.stdout.write("Use --save to update database")

        else:
            raise CommandError("Cannot fetch TSV file")
