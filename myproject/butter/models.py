from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    
    class Meta:
        ordering = ['code']

class Day(models.Model):
    county = models.ForeignKey(County, related_name='days', on_delete=models.CASCADE)
    date = models.DateField()
    cases = models.IntegerField()
    deaths = models.IntegerField()

    class Meta:
        unique_together = ['county', 'date']
        ordering = ['date']

