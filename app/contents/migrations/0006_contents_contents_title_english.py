# Generated by Django 2.2.11 on 2020-03-30 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0005_auto_20200326_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='contents_title_english',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]