# Generated by Django 5.0.6 on 2024-07-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_alter_listing_current_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="price",
            field=models.DecimalField(decimal_places=1, default=0, max_digits=12),
        ),
    ]
