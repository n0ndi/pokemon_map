# Generated by Django 3.1.14 on 2023-04-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0007_pokemon_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]