import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from butter.models import County, Day

import csv

from datetime import datetime, timedelta, date

yesterday = date.today() - timedelta(days=3)

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
        in_db = bool(County.objects.filter(code=fips))
        if not in_db:
            name = row['county']
            county = County(name=name, code=fips)
            county.save()
        countyid = County.objects.get(code=fips)
        day_in_db = Day.objects.filter(county=countyid, date=date)
        cases = row['cases']
        deaths = row['deaths']
        if not bool(day_in_db):
            day = Day(county=countyid, date=date, cases=cases, deaths=deaths)
            day.save()
        else:
            day = day_in_db[0]
            day.cases = cases
            day.deaths = deaths
            day.save()
