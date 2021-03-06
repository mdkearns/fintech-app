# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 19:44
# Generated by Django 1.11.6 on 2017-11-06 17:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20171030_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportName', models.CharField(default='NO_NAME', max_length=50)),
                ('timeStamp', models.DateField(blank=True, null=True)),
                ('companyName', models.CharField(max_length=50)),
                ('companyPhone', models.CharField(max_length=12)),
                ('companyLocation', models.CharField(max_length=50)),
                ('companyCountry', models.CharField(choices=[('AD', 'Andorra'), ('AF', 'Afghanistan'), ('AG', 'Antigua and Barbuda'), ('AL', 'Albania'), ('AM', 'Armenia'), ('AO', 'Angola'), ('AR', 'Argentina'), ('AT', 'Austria'), ('AU', 'Australia'), ('AZ', 'Azerbaijan'), ('BB', 'Barbados'), ('BD', 'Bangladesh'), ('BE', 'Belgium'), ('BF', 'Burkina Faso'), ('BG', 'Bulgaria'), ('BH', 'Bahrain'), ('BI', 'Burundi'), ('BJ', 'Benin'), ('BN', 'Brunei Darussalam'), ('BO', 'Bolivia'), ('BR', 'Brazil'), ('BS', 'Bahamas'), ('BT', 'Bhutan'), ('BW', 'Botswana'), ('BY', 'Belarus'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CD', 'Democratic Republic of the Congo'), ('CG', 'Republic of the Congo'), ('CL', 'Chile'), ('CM', 'Cameroon'), ('CN', "People's Republic of China"), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('CV', 'Cape Verde'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DE', 'Germany'), ('DJ', 'Djibouti'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EE', 'Estonia'), ('EG', 'Egypt'), ('ER', 'Eritrea'), ('ET', 'Ethiopia'), ('FI', 'Finland'), ('FJ', 'Fiji'), ('FR', 'France'), ('GA', 'Gabon'), ('GE', 'Georgia'), ('GH', 'Ghana'), ('GM', 'The Gambia'), ('GN', 'Guinea'), ('GR', 'Greece'), ('GT', 'Guatemala'), ('GT', 'Haiti'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('ID', 'Indonesia'), ('IE', 'Republic of Ireland'), ('IL', 'Israel'), ('IN', 'India'), ('IQ', 'Iraq'), ('IR', 'Iran'), ('IS', 'Iceland'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JO', 'Jordan'), ('JP', 'Japan'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KI', 'Kiribati'), ('KP', 'North Korea'), ('KR', 'South Korea'), ('KW', 'Kuwait'), ('LB', 'Lebanon'), ('LI', 'Liechtenstein'), ('LR', 'Liberia'), ('LS', 'Lesotho'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('LV', 'Latvia'), ('LY', 'Libya'), ('MG', 'Madagascar'), ('MH', 'Marshall Islands'), ('MK', 'Macedonia'), ('ML', 'Mali'), ('MM', 'Myanmar'), ('MN', 'Mongolia'), ('MR', 'Mauritania'), ('MT', 'Malta'), ('MU', 'Mauritius'), ('MV', 'Maldives'), ('MW', 'Malawi'), ('MX', 'Mexico'), ('MY', 'Malaysia'), ('MZ', 'Mozambique'), ('NA', 'Namibia'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NI', 'Nicaragua'), ('NL', 'Kingdom of the Netherlands'), ('NO', 'Norway'), ('NP', 'Nepal'), ('NR', 'Nauru'), ('NZ', 'New Zealand'), ('OM', 'Oman'), ('PA', 'Panama'), ('PE', 'Peru'), ('PG', 'Papua New Guinea'), ('PH', 'Philippines'), ('PK', 'Pakistan'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PW', 'Palau'), ('PY', 'Paraguay'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('SA', 'Saudi Arabia'), ('SB', 'Solomon Islands'), ('SC', 'Seychelles'), ('SD', 'Sudan'), ('SE', 'Sweden'), ('SG', 'Singapore'), ('SI', 'Slovenia'), ('SK', 'Slovakia'), ('SL', 'Sierra Leone'), ('SM', 'San Marino'), ('SN', 'Senegal'), ('SO', 'Somalia'), ('SR', 'Suriname'), ('SY', 'Syria'), ('TG', 'Togo'), ('TH', 'Thailand'), ('TJ', 'Tajikistan'), ('TM', 'Turkmenistan'), ('TN', 'Tunisia'), ('TO', 'Tonga'), ('TR', 'Turkey'), ('TT', 'Trinidad and Tobago'), ('TV', 'Tuvalu'), ('TZ', 'Tanzania'), ('UA', 'Ukraine'), ('UG', 'Uganda'), ('US', 'United States'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('VU', 'Vanuatu'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'), ('DZ', 'Algeria'), ('BA', 'Bosnia and Herzegovina'), ('KH', 'Cambodia'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('KM', 'Comoros'), ('HR', 'Croatia'), ('TL', 'East Timor'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('GD', 'Grenada'), ('KZ', 'Kazakhstan'), ('LA', 'Laos'), ('FM', 'Federated States of Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('MA', 'Morocco'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('RS', 'Serbia'), ('ZA', 'South Africa'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SZ', 'Swaziland'), ('CH', 'Switzerland'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom')], default='US', max_length=3)),
                ('sector', models.CharField(max_length=50)),
                ('industry', models.CharField(max_length=50)),
                ('accessType', models.CharField(choices=[('private', 'private'), ('public', 'public')], default='public', max_length=7)),
                ('companyUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMadeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
