# Generated by Django 4.2.2 on 2023-11-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_news_data_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news_data",
            name="img",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
