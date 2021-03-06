# Generated by Django 3.1 on 2020-08-24 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_add_vendor_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorical_dose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'מינון קטגורי',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'חברה',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'מינון בפועל',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'תצורה',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Kind_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'שם הזן',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturing_country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'ארץ ייצור',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'סוג',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('pharma_code', models.CharField(blank=True, max_length=45, null=True)),
                ('page_num', models.CharField(blank=True, max_length=45, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='Amount')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('comments', models.TextField(blank=True)),
                ('categorical_dose', models.ForeignKey(blank=True, help_text='leave blank if unknown or same as vendor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.categorical_dose')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.company')),
                ('dose', models.ForeignKey(blank=True, help_text='leave blank if unknown or same as vendor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.dose')),
                ('formation', models.ForeignKey(blank=True, help_text='leave blank if unknown or same as vendor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.formation')),
                ('kind_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.kind_name')),
                ('m_type', models.ForeignKey(blank=True, help_text='leave blank if unknown or same as vendor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.type')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.manufacturer')),
                ('manufacturing_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.manufacturing_country')),
            ],
        ),
    ]
