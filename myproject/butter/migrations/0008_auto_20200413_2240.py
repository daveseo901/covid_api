# Generated by Django 3.0.5 on 2020-04-13 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0007_auto_20200411_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='butter.County'),
        ),
    ]