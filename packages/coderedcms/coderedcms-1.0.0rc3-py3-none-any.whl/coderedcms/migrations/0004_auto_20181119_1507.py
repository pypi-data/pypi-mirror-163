# Generated by Django 2.0.9 on 2018-11-19 20:07

import coderedcms.blocks.base_blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('coderedcms', '0003_auto_20180912_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleApiSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_maps_api_key', models.CharField(blank=True, help_text='The API Key used for Google Maps.', max_length=255, verbose_name='Google Maps API Key')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Google API Settings',
            },
        ),
    ]
