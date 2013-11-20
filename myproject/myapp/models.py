from django.db import models
import os.path
from django.contrib.auth.models import User as BaseUser
# Create your models here.

class Document(models.Model):
	user = models.ForeignKey(BaseUser)
	docfile = models.FileField(upload_to='files/')

	def __str__(self):
   	    return str(self.user)+ " "+ str(os.path.basename(self.docfile.name))

   	@property
   	def filename(self):
   	    return os.path.basename(self.docfile.name) 
  
   	