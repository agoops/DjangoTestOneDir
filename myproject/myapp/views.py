
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from models import Document


def temp(request):
	print "temp entered"
	print request
	return HttpResponse("Hello from django")

	
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
    		print request.user.username
    		user = User.objects.get(username__exact='ankitgupta')
	    	
	    	qs = Document.objects.filter(user=user)
	    	qs_list = list(qs)
	    	print "Keys in this post"
	    	for k in request.FILES:

	    		print k 
	    		whatFilenameWouldBe = str(user)+'/'+k

	    		fileFound=False
	    		for xx in qs: 
	    			fileNameOnSystem = str(xx.docfile.name)
	    			print whatFilenameWouldBe
	    			print fileNameOnSystem
	    			if fileNameOnSystem == whatFilenameWouldBe:
	    				print "File exists"
	    				xx.docfile.delete()
	    				xx.delete()
	    				qs_list.remove(xx)
	    				actualFile=request.FILES[k]
	    				timestamp = int(float(request.POST.get(k)))
	    				print timestamp


	    				newdoc=Document(user=user, timestamp=timestamp,localpath=k,docfile=actualFile)
	    				newdoc.save()
	    				fileFound=True
	    		

	    		if fileFound==False:
	    			print "New file"
	    			timestamp=int(float(request.POST.get(k)))
	    			newdoc = Document(user=user, timestamp=timestamp,localpath=k, docfile=request.FILES[k])
	    			newdoc.save()


    		for element in qs_list:
    			element.docfile.delete()
    			element.delete()
    			print "deleted" + str(element)



    		docsByThisUser = Document.objects.filter(user=user)

	    	print "\nDocs by this user"
	    	for f in docsByThisUser:
	    		print f.docfile.name
	    		# f.docfile.delete()
	    		# f.delete()
	    	print "---"

	    	# for f in docsByThisUser:
	    	# 	print f.filename
	    	
	    	# str(request.FILES['docfile'].name)

	    	# newdoc.save()
	    	# print("FileUploaded: " + postFilename)
	    	# printAllDocsByUser(user)
	    	return HttpResponse("Files uploaded")



    else:
        return HttpResponse("Hit /upload with no post request")

def get_files(request):
	user = User.objects.get(username__exact="ankitgupta")
	print "---"
	print str(request.user.username)
	print "---"
	qs = Document.objects.filter(user=user)
	listOfFiles = []
	for f in qs:
		listOfFiles.append(str(f.filename))

	data={"files":listOfFiles}
	return HttpResponse(str(data))

    
