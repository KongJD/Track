from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
# Register your models here.

@admin.register(Sampling)
class SamplingAdmin(admin.ModelAdmin):
    #list_display = ['id','sid','usern', 'strain', 'projectid', 'sampleName','Sampler','isolation_time','medium','temperature','oxygen','source','source_detail','city','GPS','remarks']
    #list_display='__all__'
    list_display=['id','usern','sampleNo', 'collectionTime', 'sourceType','city','productName','organizationId']
    list_display_links = ['id','usern']
    list_filter = ['usern', 'sampleNo', 'collectionTime', 'sourceType','city','productName','organizationId']
    #readonly_fields = ['id','sid','Sampler','create_time','updated_time']

    def get_queryset(self, request):
        return Sampling.objects_all.all()

