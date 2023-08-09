from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import Participant, FreshmanTicket, GeneralTicket

# Register your models here.

class ParticipantResource(resources.ModelResource):
    general_ticket_buyer = fields.Field(
        column_name='general_ticket_buyer',
        attribute='general_ticket__buyer',  # ForeignKey의 buyer 필드에 접근
    )

    class Meta:
        model = Participant
        exclude = ('id',)  # id 필드 제외
        fields = ('name', 'phone_num', 'general_ticket_buyer')

class FreshmanTicketResource(resources.ModelResource):
    class Meta:
        model = FreshmanTicket
        exclude = ('updated',)  # updated 필드 제외

class GeneralTicketResource(resources.ModelResource):
    class Meta:
        model = GeneralTicket
        exclude = ('updated',)  # updated 필드 제외
        

@admin.register(models.Participant)
class ParticipantAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name','phone_num')
    resource_class = ParticipantResource  # ParticipantResource를 사용하도록 설정
    pass

@admin.register(models.FreshmanTicket)
class FreshmanTicketAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('buyer','phone_num','major','student_id','meeting')
    resource_class = FreshmanTicketResource  # FreshmanTicketResource 설정
    pass

@admin.register(models.GeneralTicket)
class GeneralTicketAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('buyer','phone_num','member','price')
    resource_class = GeneralTicketResource  # GeneralmanTicketResource 설정
    pass

@admin.register(models.OrderTransaction)
class OrderTransactionAdmin(admin.ModelAdmin):
    pass