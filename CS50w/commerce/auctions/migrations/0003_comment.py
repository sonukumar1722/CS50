# Generated by Django 4.1 on 2022-09-07 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_create_id_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('comment', models.TextField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('commenter', models.CharField(max_length=64)),
            ],
        ),
    ]
