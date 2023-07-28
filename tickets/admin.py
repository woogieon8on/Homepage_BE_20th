from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.GeneralTicket)
class GeneralTicketAdmin(admin.ModelAdmin):
    pass

@admin.register(models.FreshmanTicket)
class FreshmanTicketAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass