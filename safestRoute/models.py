from django.db import models

# Create your models here.

class AccidentData(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	count = models.PositiveIntegerField(default=1)
	class Meta:
		unique_together = ('latitude','longitude')
