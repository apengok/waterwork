# Generated by Django 2.0 on 2019-07-24 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmam', '0002_station_bigmeter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='bigmeter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='legacy.Bigmeter'),
        ),
    ]