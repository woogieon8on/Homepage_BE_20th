from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.

@admin.register(models.ApplyForm)
class ApplyFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name','phone_num','birthdate','gender','address','first_preference',
                    'second_preference','play_instrument','motive')
    pass