# Generated by Django 4.1 on 2022-11-18 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_booksinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date_of_issue',
            field=models.DateField(blank=True, default='1990-12-05'),
        ),
    ]
