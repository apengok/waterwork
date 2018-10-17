# Generated by Django 2.0 on 2018-10-17 21:02

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entm', '0002_auto_20180826_0107'),
        ('dmam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='Name', max_length=64, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=128, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('belongto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community', to='entm.Organizations')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dmam.VCommunity')),
            ],
            options={
                'db_table': 'vcommunity',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VConcentrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='Name', max_length=64, null=True)),
                ('commaddr', models.CharField(blank=True, max_length=50, null=True, verbose_name='通讯识别码')),
                ('belongto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concentrator', to='entm.Organizations')),
                ('communityid', models.ManyToManyField(to='dmam.VCommunity')),
            ],
            options={
                'db_table': 'vconcentrator',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VWatermeter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='Name', max_length=64, null=True)),
                ('waterid', models.IntegerField(blank=True, db_column='WaterId', max_length=30, null=True)),
                ('wateraddr', models.CharField(blank=True, db_column='WaterAddr', max_length=30, null=True)),
                ('belongto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watermeter', to='entm.Organizations')),
                ('communityid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watermeter', to='dmam.VCommunity')),
            ],
            options={
                'db_table': 'vwatermeter',
                'managed': True,
            },
        ),
    ]
