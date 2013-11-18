
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from models import Document



def index(request):
	print 'Heyjkfdlsajfks'
	return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if (user is not None):
			return HttpResponse("User logged in!", status = 200)
		else:
			print ("Login failed")
			return HttpResponse("Login failed", status = 404)


def signup(request):
	#return HttpResponse("And this is the signup page!")
	if request.method == "POST":
		username = request.POST['username']

		if User.objects.filter(username=username).count():
			print 'User already exists'
			return HttpResponse("User already exists.")
		else:
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			password = request.POST['password']
			print first_name, last_name,email,password
			user = User.objects.create_user(username,email,password)
			user.last_name = last_name
			user.first_name = first_name
			user.save()


	#return render_to_response("myapp/main.html")
		return HttpResponse("User created!")
	#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
	#return render(request, 'polls/index.html')

def check_password(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			return HttpResponse("true")
		else:
			return HttpResponse("false")

def change_password(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['new_password']
		u = User.objects.get(username__exact=username)
		u.set_password(password)
		u.save()
		return HttpResponse("Password changed!")

def printAllDocsByUser(user=None):
	print str(user)
	docs = Document.objects.filter(user=user)
	print docs

def upload(request):
    # Handle file upload
    if request.method == 'POST':
    	if request.user.is_authenticated:
    		user = User.objects.get(username__exact='joe')
    		print str(user)
	    	# try:
	    	newdoc = Document(user = user, docfile = request.FILES['docfile'])
	    	newdoc.save()

	    	print("File uploaded?")
	    	print str(newdoc)
	    	printAllDocsByUser(user)
	    	return HttpResponse("File uploaded")
	        # except Exception, e:
	        	# print(str(e))
	        	# return HttpResponse("Error occurred.")
    else:
        return HttpResponse("Hit /upload with no post request")

    
