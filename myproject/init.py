import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from butter.models import County, Day

c = County.objects.get(code=42069)
d = Day.objects.create(county=c, date="1989-04-20", cases=690, deaths=10)
d.save()
