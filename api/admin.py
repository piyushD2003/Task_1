from django.contrib import admin
from .models import User, Doctor, Records
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('Doctorname', 'email')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'date')

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Records, RecordAdmin)