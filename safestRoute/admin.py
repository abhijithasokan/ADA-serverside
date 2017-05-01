from django.contrib import admin

# Register your models here.
from .models import AccidentData

class AccidentDataAdminModel(admin.ModelAdmin):
	class Meta:
		model = AccidentData
	list_display = ['latitude','longitude','count']

admin.site.register(AccidentData,AccidentDataAdminModel)