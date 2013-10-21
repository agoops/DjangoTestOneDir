
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response



def index(request):
	print 'Heyjkfdlsajfks'
	return HttpResponse("Hello, world. You're at the polls index.")

def signup(request):
	#return HttpResponse("And this is the signup page!")
	if request.method == "POST":
		username = request.POST['username']

		if User.objects.filter(username=username).count():
			print 'User already exists'
			return HttpResponse("User already exists")
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


# def lexusadduser(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             new_user = User.objects.create_user(**form.cleaned_data)
#             login(new_user)
#             # redirect, or however you want to get to the main view
#             return HttpResponseRedirect('main.html')
#     else:
#         form = UserForm() 

#     return render(request, 'adduser.html', {'form': form}) # Create your views here.
