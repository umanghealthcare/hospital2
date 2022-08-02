from django.contrib import admin
from .models import User,Contact,Doctor_profile,Appointment,cancelappointment,doctorcancelappointment,Transaction,Healthprofile
# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Doctor_profile)
admin.site.register(Appointment)
admin.site.register(cancelappointment)
admin.site.register(doctorcancelappointment)
admin.site.register(Transaction)
admin.site.register(Healthprofile)
