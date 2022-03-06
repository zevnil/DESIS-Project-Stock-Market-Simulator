# Generated by Django 4.0.3 on 2022-03-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stockId', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('stockName', models.CharField(max_length=128, unique=True)),
                ('fullCompanyName', models.CharField(max_length=128)),
                ('currentSharePrice', models.DecimalField(decimal_places=3, max_digits=16)),
                ('sharesOutstanding', models.IntegerField()),
                ('lastTradedAt', models.DateField(auto_now=True)),
            ],
        ),
    ]
