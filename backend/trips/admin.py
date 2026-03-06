from django.contrib import admin

from .models import ItineraryItem, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["destination", "start_date", "end_date", "budget", "budget_currency", "created_at"]
    list_filter = ["budget_currency"]
    search_fields = ["destination", "purpose"]
    date_hierarchy = "created_at"


@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ["trip", "day", "time", "activity"]
    list_filter = ["day"]
    search_fields = ["activity", "notes"]
