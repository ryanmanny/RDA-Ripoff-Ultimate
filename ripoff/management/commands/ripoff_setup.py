from django.core.management.base import BaseCommand, CommandError

from ripoff.models import RDAPlan


class Command(BaseCommand):
    help = 'Initializes the DB with some default models'

    def handle(self, *args, **options):
        # Default RDA Plans
        RDAPlan.plans.bulk_create([  # Optimized!
            RDAPlan(plan=0, base_cost=0, dollars=0),
            RDAPlan(plan=1, base_cost=944, dollars=905),
            RDAPlan(plan=2, base_cost=944, dollars=1180),
            RDAPlan(plan=3, base_cost=944, dollars=1405),
        ])

        self.stdout.write("Initialized default RDA Plans")
