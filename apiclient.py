import requests
from offer_sync.models import CustomerConfiguration
from realty.models import Offer
import json

class OfferSyncClient:
    def __init__(self, customer_name):
        """
        Initialize the client with a specific customer's configuration.
        """
        try:
            config = CustomerConfiguration.objects.get(name=customer_name, is_active=True)
        except CustomerConfiguration.DoesNotExist:
            raise ValueError("Configuration for customer '" + customer_name + "' does not exist or is inactive.")

        self.api_base_url = config.api_base_url
        self.api_token = config.api_token
        self.post_codes = config.get_post_codes()
        self.contact_types = config.get_contact_types()
        self.headers = {"Authorization": "Token " + str(self.api_token),
            "Content-Type": "application/json",
        }

    def sync_offers(self):
        """
        Synchronize offers for the configured customer.
        """
        for contact_type in self.contact_types:
            self._sync_offers_by_contact_type(contact_type)

    def _sync_offers_by_contact_type(self, contact_type):
        """
        Sync offers for a specific contact type.
        """
        # Fetch offers based on the configuration's post codes and contact type
        # Example logic:
        print("Syncing offers for contact type: " + contact_type + "")
        # Add your synchronization logic here
        offers = Offer.objects.filter(contact_type=contact_type, post_code__in=self.post_codes, section="sale")
        print("Syncing " + str(offers.count()) + " offers for contact type: " + contact_type + "")
        for offer in offers:
            self._send_offer_to_api(offer)

    def _send_offer_to_api(self, offer):
        """
        Stuur een enkele offer naar de API.
        """
        """payload = {
            "title": offer.title,
            "realty_type": offer.realty_type,
            "section": offer.section,
            "post_code": offer.post_code,
            "location": offer.location,
            "address": offer.address,
            "price": str(offer.price) if offer.price else None,
            "total_surface": offer.total_surface,
            "short_description": offer.short_description,
            "number_of_bedrooms": offer.number_of_bedrooms,
            "bathrooms": offer.bathrooms,
            "type_of_construction": offer.type_of_construction,
            "phone": offer.contact.phone_1 if offer.contact else None,
            "source": offer.source,
            "contact_type": offer.contact_type,
            "image_url": offer.main_image,
            "property_url": offer.property_url,
            "monthly_costs": offer.monthly_costs,
            "mobile": offer.contact.mobile if offer.contact else None,
            "created": offer.created.isoformat() if offer.created else None,
        } """

        payload = {
            "title": offer.title or "",
            "realty_type": offer.realty_type or "",
            "section": offer.section or "",
            "post_code": offer.post_code or "",
            "location": offer.location or "",
            "address": offer.address or "",
            "price": str(offer.price) if offer.price else None,  # Convert Decimal to string
            "total_surface": offer.total_surface or "",
            "short_description": offer.short_description or "",
            "number_of_bedrooms": offer.number_of_bedrooms or 0,
            "bathrooms": offer.bathrooms or 0,
            "type_of_construction": offer.type_of_construction or "",
            "phone": offer.contact.phone_1 if offer.contact else None,
            "contact_type": offer.contact_type or "",
            "image_url": offer.main_image or "",
            "property_url": offer.property_url or "",
            "monthly_costs": str(offer.monthly_costs) if offer.monthly_costs else None,
            "mobile": offer.contact.mobile if offer.contact else None,
            "created": offer.created.isoformat() if offer.created else None,
        }

        try:
            #import pdb;pdb.set_trace();
            response = requests.post(self.api_base_url, json=payload, headers=self.headers)
            print(response)
            print(response.content)
            response.raise_for_status()
            print("Offer " + str(offer.id) + " successfully synced.")
        except requests.exceptions.RequestException as e:
            print("Failed to sync offer " + str(offer.id))

        
