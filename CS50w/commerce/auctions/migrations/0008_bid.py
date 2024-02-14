# Generated by Django 4.1 on 2022-09-10 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_watchlist_match_alter_watchlist_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('ids', models.JSONField(null=True)),
                ('bidder', models.CharField(max_length=64)),
                ('bid_value', models.DecimalField(decimal_places=2, max_digits=16)),
            ],
        ),
    ]