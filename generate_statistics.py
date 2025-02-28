# your_app/management/commands/generate_historical_statistics.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from lead.models import DailyStatistics, Offer
from django.conf import settings

NUMBER_OF_DAYS = 91

class Command(BaseCommand):
    help = 'Generate historical statistics for the past 60 days'

    def handle(self, *args, **options):
        # Set the end date to today
        end_date = timezone.now().date()
        print(end_date)        
        # Set the start date to 60 days before today
        start_date = end_date - timedelta(days=settings.NUMBER_OF_DAYS)
        print(start_date)
        # Loop through each date in the range
        for day in range(0, settings.NUMBER_OF_DAYS + 1):  # 91 to include today
            date = start_date + timedelta(days=day)

            # Define the start and end of the current day
            start_of_day = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
            end_of_day = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.max.time()))

            # Get or create the DailyStatistics record for this date
            stats, created = DailyStatistics.objects.get_or_create(date=date)

            # Calculate statistics for this date using date ranges
            stats.new_offers_count = Offer.objects.filter(
                created__range=(start_of_day, end_of_day)
            ).count()

            stats.contacted_offers_count = Offer.objects.filter(
                contacted=True, last_status_update__range=(start_of_day, end_of_day)
            ).count()

            # Save the statistics
            stats.save()

            # Output progress message
            print('Statistics generated for ' + str(date))
        
        print('Successfully generated historical statistics for the past 60 days')
