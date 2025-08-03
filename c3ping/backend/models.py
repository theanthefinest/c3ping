from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(default=0)
    url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name