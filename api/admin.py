from django.contrib import admin
from .models import User, Doctor
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('Doctorname', 'email')

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)