import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from butter.models import County, Day

import csv

from datetime import datetime, timedelta, date

yesterday = date.today() - timedelta(days=1)

with open('/home/davidseo901/project/data/us-counties.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        date = row['date']
        compdate = datetime.strptime(date, '%Y-%m-%d').date()
        if compdate < yesterday:
            continue
        fips = row['fips']
        if fips == '':
            continue
        in_db = County.objects.filter(code=fips)
        in_db = bool(in_db)
        if not in_db:
            name = row['county']
            county = County(name=name, code=fips)
            county.save()
        countyid = County.objects.get(code=fips)
        cases = row['cases']
        deaths = row['deaths']
        day = Day(county=countyid, date=date, cases=cases, deaths=deaths)
        day.save()
