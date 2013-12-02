from django.db import models
import os.path
from django.contrib.auth.models import User as BaseUser
# Create your models here.

def base(self, filename):
    url = "%s/%s" % (self.user.username, self.localpath)
    return url

class Document(models.Model):
	user = models.ForeignKey(BaseUser)
	localpath = models.CharField(max_length=100)
	docfile = models.FileField(upload_to=base)

	def __str__(self):
   	    return str(self.user)+ " "+ str(self.docfile.name)

   	@property
   	def filename(self):
   	    return self.localpath
  
   	