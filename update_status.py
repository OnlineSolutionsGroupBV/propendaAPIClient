# Django Command to fetch data from the view
# Save this in a management/commands directory as `fetch_offer_status.py`
import requests
from django.core.management.base import BaseCommand
from lead.models import Offer

class Command(BaseCommand):
    help = 'Fetches offer status information from the specified view for all Offers with new or None status.'

    def handle(self, *args, **kwargs):
        url = 'https://be.propenda.com/offer_sync/get_offer_status/'
        status_key = 'created_key_for_auth'

        # Query all Offer objects with status "new" or None
        offers = Offer.objects.filter(status__in=['new', 'None'])

        if not offers.exists():
            self.stdout.write(self.style.WARNING('No offers found with status "new" or "None".'))
            return
        #import pdb;pdb.set_trace()
        for offer in offers:
            property_url = offer.property_url
            api_url = f"{url}?status_key={status_key}&property_url={property_url}"
            print(api_url)
            try:
                response = requests.get(api_url)

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"Success for {property_url}:"))
                    self.stdout.write(str(response.json()))
                    # Update the status field in the Offer model
                    offer.status = response.json().get('status', offer.status)
                    offer.save()
                elif response.status_code == 403:
                    self.stderr.write(self.style.ERROR(f"Error for {property_url}: Invalid or missing status_key parameter."))
                elif response.status_code == 400:
                    self.stderr.write(self.style.ERROR(f"Error for {property_url}: property_url parameter is required."))
                elif response.status_code == 404:
                    self.stderr.write(self.style.ERROR(f"Error for {property_url}: OfferStatus object not found."))
                else:
                    self.stderr.write(self.style.ERROR(f"Unexpected Error for {property_url}: {response.status_code}"))
            except requests.RequestException as e:
                self.stderr.write(self.style.ERROR(f"Request failed for {property_url}: {e}"))



