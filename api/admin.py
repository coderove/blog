from django.contrib import admin

# Register your models here.
from api.models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ['email','content','create_date']


admin.site.register(Email,EmailAdmin)