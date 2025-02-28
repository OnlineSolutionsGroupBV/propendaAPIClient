from django.core.management.base import BaseCommand
from offer_sync.models import CustomerConfiguration
from offer_sync.management.commands.apiclient import OfferSyncClient

class Command(BaseCommand):
    help = 'Synchronize offers for all active customers'

    def handle(self, *args, **kwargs):
        customers = CustomerConfiguration.objects.filter(is_active=True)
        if not customers.exists():
            print("No active customer configurations found.")
            return

        for customer in customers:
            print("Starting sync for customer: " + customer.name + "")
            try:
                #import pdb;pdb.set_trace();
                client = OfferSyncClient(customer.name)
                client.sync_offers()
                print("Successfully synced offers for customer: " + customer.name + "")
            except Exception as e:
                print("Failed to sync for customer " + customer.name + "")
