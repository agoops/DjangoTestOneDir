__author__ = 'Peter'
from django.contrib import admin
from django.contrib.auth.models import User
from models import Document


#class DocumentAdmin(admin.ModelAdmin):
   # fields = User.objects.all()

admin.site.register(Document)

# Register your models here.