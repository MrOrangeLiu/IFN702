# Generated by Django 2.1 on 2018-10-26 18:29

from django.db import migrations
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='file',
            field=djongo.models.fields.ArrayReferenceField(on_delete=django.db.models.deletion.CASCADE, to='fileuploads.File'),
        ),
    ]