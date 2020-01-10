import requests
from django.core.management.base import BaseCommand, CommandError

# from events.models import Event

from staff.logics import all_inconsistent_events

TSV_LINK = "https://docs.google.com/spreadsheets/d/1kJHQVorZv4iGmaNtr0Xlf6JwOqiU_MAQOD1noJRMEyU/export?format=tsv"


class Command(BaseCommand):
    help = "Fetch the official schedule and find inconsistencies"

    def handle(self, *args, **kwargs):
        response = requests.get(TSV_LINK)
        data = str(response.content)
        if response.status_code == 200:
            e = all_inconsistent_events(data)
            if e:
                self.stdout.write(", ".join(map(str, [x.id for x in e])))
                self.stdout.write(
                    self.style.WARNING("{} inconsistencies found".format(len(e)))
                )
            else:
                self.stdout.write(self.style.SUCCESS("No inconsistencies found"))
        else:
            raise CommandError("Cannot fetch TSV file")
