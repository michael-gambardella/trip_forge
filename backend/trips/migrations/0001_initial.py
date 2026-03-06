import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("destination", models.CharField(max_length=255)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("budget", models.DecimalField(decimal_places=2, max_digits=10)),
                ("budget_currency", models.CharField(default="USD", max_length=3)),
                ("purpose", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ItineraryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.PositiveIntegerField()),
                ("time", models.CharField(max_length=10)),
                ("activity", models.CharField(max_length=500)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itinerary_items",
                        to="trips.trip",
                    ),
                ),
            ],
            options={
                "ordering": ["day", "time"],
            },
        ),
    ]
