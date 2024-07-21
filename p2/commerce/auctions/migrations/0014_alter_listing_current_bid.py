# Generated by Django 5.0.6 on 2024-07-11 19:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0013_alter_listing_current_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="current_bid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="listing",
                to="auctions.bid",
            ),
        ),
    ]
