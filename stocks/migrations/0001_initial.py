# Generated by Django 2.0.4 on 2018-06-24 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=64)),
                ('last', models.CharField(max_length=64)),
                ('custUserID', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=64, null=True)),
                ('symbolPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('symbolQty', models.IntegerField()),
                ('symbolNet', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('symbolCust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Customer')),
            ],
        ),
    ]
