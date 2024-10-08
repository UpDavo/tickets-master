# Generated by Django 4.1.13 on 2024-09-30 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artist_name', models.CharField(max_length=255)),
                ('artist_gender', models.CharField(max_length=255)),
                ('artist_age', models.IntegerField()),
                ('artist_country', models.CharField(max_length=255)),
                ('artist_followers', models.IntegerField()),
                ('artist_genres', models.CharField(max_length=255)),
                ('event_city', models.CharField(max_length=255)),
                ('event_country', models.CharField(max_length=255)),
                ('event_venue', models.CharField(max_length=255)),
                ('artist_popularity', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
