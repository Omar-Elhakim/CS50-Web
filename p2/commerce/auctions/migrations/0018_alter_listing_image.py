# Generated by Django 5.0.6 on 2024-07-12 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0017_alter_listing_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="image",
            field=models.URLField(max_length=2000),
        ),
    ]