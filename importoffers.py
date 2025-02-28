import json
import os
from django.core.management.base import BaseCommand
from lead.models import Offer

# import offers for test data
# Django command
class Command(BaseCommand):
    help = 'Import offers from a JSON file in the data/ folder into the Offer model'

    def handle(self, *args, **kwargs):
        # Define the path to the JSON file
        json_file_path = 'data/bauwens.14dec.2024.json' #'data/bauwens.json'

        # Check if the file exists
        if not os.path.exists(json_file_path):
            self.stderr.write(f"File not found: {json_file_path}")
            return

        # Load the JSON data
        self.stdout.write("Loading data from the JSON file...")
        try:
            with open(json_file_path, 'r') as json_file:
                offers_data = json.load(json_file)
        except json.JSONDecodeError as e:
            self.stderr.write(f"Error reading JSON file: {e}")
            return

        # Populate the database
        import pdb;pdb.set_trace()
        for offer_data in offers_data:
            try:
                fields = offer_data["fields"]  # Access the nested fields
                print(fields)
                offer, created = Offer.objects.update_or_create(
                    property_url=fields["property_url"],
                    defaults={
                        'title': fields["title"],
                        'realty_type': fields["realty_type"],
                        'section': fields["section"],
                        'post_code': fields["post_code"],
                        'location': fields["location"],
                        'address': fields["address"],
                        'price': fields["price"],
                        'total_surface': fields["total_surface"],
                        'livable_surface': fields["livable_surface"],
                        'short_description': fields["short_description"],
                        'number_of_bedrooms': fields["number_of_bedrooms"],
                        'bathrooms': fields["bathrooms"],
                        'furnished': fields["furnished"],
                        'type_of_construction': fields["type_of_construction"],
                        'monthly_costs': fields["monthly_costs"],
                        'for_index': fields.get("for_index", True),
                        'hash': fields.get("hash", ""),
                        'created': fields["created"],
                        'last_status_update': fields["last_status_update"],
                        'contact_type': fields["contact_type"],
                        'status': fields.get("status", "new"),
                        'phone': fields["phone"],
                        'mobile': fields["mobile"],
                        'contacted': fields.get("contacted", False),
                        'contacted_date': fields["contacted_date"],
                        'nota': fields["nota"],
                        'image_url': fields["image_url"],
                        'deal_stage': fields.get("deal_stage", "introduction_qualification"),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created offer: {fields["title"]}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated offer: {fields["title"]}'))
            except KeyError as e:
                self.stderr.write(f"Missing key in data: {e}")
            except Exception as e:
                self.stderr.write(f"Error saving offer: {e}")
        self.stdout.write("Data import completed successfully.")


