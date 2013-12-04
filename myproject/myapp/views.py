
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.core.files import File
from models import Document
import ast
import os, mimetypes

def temp(request):
	print "temp entered"
	print request
	return HttpResponse("Hello from django")

def checkForUpdates(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username=username,password=password)

	timestampMap = ast.literal_eval(request.POST['timestampMap'])
	
	filesByThisUser = Document.objects.filter(user=user)

	# converting timestamps to ints
	print "Files and timestamps sent by local"
	for k in timestampMap:
		timestampMap[k]=int(float(timestampMap[k]))
		print k,timestampMap[k]
	print 
	print 

	serverTimestampMap = {}
	serverIdMap={}
	filesByThisUser = list(Document.objects.filter(user=user))
	print "Files and timestamps on server"

	for doc in filesByThisUser:
		serverTimestampMap[doc.filename] = int(doc.timestamp)
		serverIdMap[doc.filename]= doc.id
		print doc.filename + " " +str(doc.timestamp) + " "+ str(doc.id)

	filesToDelete=[]
	filesToUpdate=[]	
	print "\n Files to send back to client"

	for k in timestampMap:
		if k in serverTimestampMap and serverTimestampMap[k]>timestampMap[k]:
			filesToUpdate.append(serverIdMap[k])
		elif k not in serverTimestampMap:
			filesToDelete.append(k)

	result = {'update': filesToUpdate, 'delete': filesToDelete}
	return HttpResponse( str(result))
	

def pull_file(request):

	fileId = int(request.POST['fileId'])
	print '\nReceived request to pull file: '  + str(fileId)
	fileToSend = Document.objects.get(id=fileId)
	path = fileToSend.docfile.path
	print path
	filename = fileToSend.filename
	print filename
	# return HttpResponse("Hey")
	httpresponse = send_file(path=path, filename=filename,timestamp=fileToSend.timestamp)
	return httpresponse


def send_file(path, filename = None, mimetype = None, timestamp=100):

	if mimetype is None:
	    mimetype, encoding = mimetypes.guess_type(filename)

	response = HttpResponse(mimetype=mimetype)
	response['Content-Disposition'] = 'attachment; filename=%s' %filename
	response['timestamp'] = timestamp
	newFile = file(path, "r")
	response.write(newFile.read())
	return response


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

    		username = request.POST['username']
    		password = request.POST['password']
    		user = authenticate(username=username,password=password)
	    	timestampMap = ast.literal_eval(request.POST['timestampMap'])

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
	    			if fileNameOnSystem == whatFilenameWouldBe and int(float(timestampMap.get(k))) == xx.timestamp:
	    				# File exists, and does not need to be updated
	    				# Remove from query set so it does not get deleted
	    				qs_list.remove(xx)
	    				fileFound = True
	    				break
	    			elif fileNameOnSystem == whatFilenameWouldBe and int(float(timestampMap.get(k))) > xx.timestamp:
	    				print "User " + user.username + " updated file: " + fileNameOnSystem
	    				xx.docfile.delete()
	    				xx.delete()
	    				qs_list.remove(xx)
	    				actualFile=request.FILES[k]
	    				timestamp = int(float(timestampMap.get(k)))


	    				newdoc=Document(user=user, timestamp=timestamp,localpath=k,docfile=actualFile)
	    				newdoc.save()
	    				fileFound=True
	    				break
	    			

	    		if fileFound==False:
	    			print "User " + user.username + " added new file: " + k
	    			timestamp=int(float(timestampMap.get(k)))
	    			newdoc = Document(user=user, timestamp=timestamp,localpath=k, docfile=request.FILES[k])
	    			newdoc.save()


    		for element in qs_list:
    			print "User " + user.username + " updated file: " + element.filename + " [DELETED]"
    			element.docfile.delete()
    			element.delete()



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

def get_list_files(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	print "---"
	print str(request.user.username)
	print "---"
	qs = Document.objects.filter(user=user)
	listOfFiles = []
	for f in qs:
		listOfFiles.append(str(f.filename))

	data={"files":listOfFiles}
	return HttpResponse(str(data))

    
