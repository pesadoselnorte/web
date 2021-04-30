# Generated by Django 3.0.7 on 2020-06-18 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extras', '0002_invoicestypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('invoice_number', models.CharField(max_length=8, verbose_name='Nro Factura')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('state', models.BooleanField(default=False)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='extras.Clients')),
                ('invoice_type_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='extras.InvoicesTypes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Comprobante',
                'verbose_name_plural': 'Comprobante',
                'ordering': ('invoice_number',),
            },
        ),
    ]