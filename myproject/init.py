import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from butter.models import County, Day

import csv

from datetime import datetime, timedelta, date

yesterday = date.today() - timedelta(days=3)
newyorklist = [36005, 36047, 36061, 36081, 36085]

with open('/home/davidseo901/project/data/us-counties.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        date = row['date']
        # compdate = datetime.strptime(date, '%Y-%m-%d').date()
        # if compdate < yesterday:
            # continue
        fips = row['fips']
        if fips == '':
            if row['county'] == 'New York City':
                precases = int(float(row['cases'])/5)
                predeaths = int(float(row['deaths'])/5)
                specialcases = int(row['cases']) % 5
                specialdeaths = int(row['deaths']) % 5
                ccount = 0
                dcount = 0
                for newfips in newyorklist:
                    cases = precases
                    deaths = predeaths
                    if ccount < specialcases:
                        cases += 1
                    if dcount < specialdeaths:
                        deaths += 1
                    ccount += 1
                    dcount += 1
                    countyid = County.objects.get(code=newfips)
                    day_in_db = Day.objects.filter(county=countyid, date=date)
                    if not bool(day_in_db):
                        day = Day(county=countyid, date=date, cases=cases, deaths=deaths)
                        day.save()
                    else:
                        day = day_in_db[0]
                        day.cases = cases
                        day.deaths = deaths
                        day.save()
            else:
                continue
        # in_db = bool(County.objects.filter(code=fips))
        # if not in_db:
            # name = row['county']
            # county = County(name=name, code=fips)
            # county.save()
        # countyid = County.objects.get(code=fips)
        # day_in_db = Day.objects.filter(county=countyid, date=date)
        # cases = row['cases']
        # deaths = row['deaths']
        # if not bool(day_in_db):
            # day = Day(county=countyid, date=date, cases=cases, deaths=deaths)
            # day.save()
        # else:
            # day = day_in_db[0]
            # day.cases = cases
            # day.deaths = deaths
            # day.save()
