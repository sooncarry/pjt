# Generated by Django 4.2.21 on 2025-05-25 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_remove_newsitem_category_remove_newsitem_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
