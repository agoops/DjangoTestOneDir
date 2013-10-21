python manage.py shell
from django.test.client import Client

c = Client()
print 'Hey from testing shell'