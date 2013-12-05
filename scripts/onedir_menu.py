import os
import urllib
import urllib2
import codecs
import requests
import time
from threading import Thread
from os import listdir
from os.path import isfile, join, isdir
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ast
from login_script import loginOrSignup

BASE_URL = ""
UPLOAD_URL = ""
GET_FILES_URL = ""
CHECK_PASSWORD_URL = ""
CHANGE_PASSWORD_URL = ""
CHECK_FOR_UPDATES_URL = ""
PULL_FILE_URL = ""
DELETE_URL = ""
USERNAME = "empty"
PASSWORD = "empty"
ROOT = ""
SYNC = False
OBSERVER = None
deleteThread = Thread()
backgroundThread = Thread()


def welcome():
	print "\n********************************************\n\nWelcome to Onedir!"\
	"\n\nHere you can view what files are synced with your account, as well as change your user settings.\n\n"
	
	main_menu2()

def main_menu2():
	try:
		while (True):
			printFiles()
			input = raw_input("\nMain Menu:Please make a selection: \n\t" \
			"[1] Toggle Sync - Currently ["+getSyncStatus()+"] \n\t" \
			"[2] Change Password\n\t" \
			"[3] Sign out\n\t")

			try:
				selection = int(input)
				if selection == 1:
					try:
						toggleSync()
					except Exception, e:
						print "toggleSync() exception"
						print e
				elif selection == 2:
					try:
						change_password()
					except Exception,e :
						print "change_passwords exception"
						print e
				elif selection == 3:
					try:
						break
					except Exception, e:
						print e
				else:
					print "Invalid input. Try again"
			except Exception, e:
				print "Invalid Input. Try again."

		signOut()

	except KeyboardInterrupt, ke: 

		global SYNC
		SYNC = False
		if backgroundThread.isAlive():
			backgroundThread.join()

def refreshFiles():
	
	global deleteThread
	while deleteThread.isAlive():
		x = 5
	timestampMap = getAllFilenamesTimestamps()
	mappingToSend = {}
	mappingToSend['username'] = USERNAME
	mappingToSend['password'] = PASSWORD
	mappingToSend['timestampMap'] = str(timestampMap)
	response = requests.post(CHECK_FOR_UPDATES_URL, data=mappingToSend)
	received = response.content
	mapping = ast.literal_eval(received)
	toUpdateList = list(mapping.get('update'))
	toDeleteList = list(mapping.get('delete'))
	if len(toDeleteList):
		deleteFiles(toDeleteList)

	for i in toUpdateList:
		pullFile(i)


def pullFile(fileId):
	data = {'fileId': fileId}
	response = requests.post(PULL_FILE_URL, data=data)
	content_disposition = response.headers['content-disposition']
	filename = content_disposition.split('; ')[1].replace('filename=', '')
	path = ROOT+'/'+filename
	content = response.content
	timestamp= int(response.headers['timestamp'])

	with open(path, "w") as fileoutput:
		fileoutput.write(content)

	atime = os.path.getatime(path)
	times = (atime,timestamp)
	os.utime(path, times)
	

def deleteFiles(fileList):
	for f in fileList:
		path = ROOT+'/'+f
		os.remove(path)

def getAllFilenamesTimestamps():
	rootfolder = ROOT
	contents = []

	for x in listdir(rootfolder):
		if x.startswith('.') or x.endswith("onedir_menu.py") or x.endswith("login_script.py") or x.endswith(".pyc") or "~" in x:
			continue
		if isfile(join(rootfolder,x)):
			contents.append(x)
		elif isdir(join(rootfolder,x)):
			folder_recurse(contents,join(rootfolder,x))

	timestampMap={}
	for f in contents:
		timestamp = str(os.path.getmtime(join(rootfolder,f)))
		timestampMap[str(f)] = timestamp

	return timestampMap

def printFiles():
	files = get_list_of_files_on_server()
	if len(files) == 0:
		print "You have no files in Onedir! Add files to your root folder and sync to your account to get started!\n"
	else:
		print "Files on Onedir:"
		for f in files:
			print "\t"+f

def getSyncStatus():
	if SYNC:
		return "ON"
	return "OFF"

def toggleSync():
	global SYNC, backgroundThread, OBSERVER
	SYNC = not SYNC
	if SYNC:
		sync();
		OBSERVER = turnOnWatchdog()
		backgroundThread = Thread(target=backgroundPoller)
		backgroundThread.start()
	else:
		if backgroundThread.isAlive():
			backgroundThread.join()
		OBSERVER.stop()
		OBSERVER.join()

def sync():
	
	rootfolder = ROOT
	contents = []

	for x in listdir(rootfolder):
		if x.startswith('.') or x.endswith("onedir_menu.py") or x.endswith("login_script.py") or x.endswith(".pyc") or "~" in x:
			continue
		if isfile(join(rootfolder,x)):
			contents.append(x)
		elif isdir(join(rootfolder,x)):
			folder_recurse(contents,join(rootfolder,x))

	fileMap = {}
	timestampMap = {}
	for f in contents:
		actualFile = codecs.open(f,'r')
		timestamp = str(os.path.getmtime(join(rootfolder,f)))
		
		fileMap[str(f)] = actualFile
		timestampMap[str(f)] = timestamp

	data = {}
	data['username'] = USERNAME
	data['password'] = PASSWORD
	data['timestampMap'] = str(timestampMap)
	response = requests.post(UPLOAD_URL, files=fileMap, data=data)
	refreshFiles()

def backgroundPoller():
	global deleteThread
	while SYNC:
		while deleteThread.isAlive():
			pass
		refreshFiles()
		time.sleep(4)
		

def folder_recurse(contents, folderpath):

	position = len(ROOT)+1

	for x in listdir(folderpath):
		if x.startswith('.'):
			continue
		if isfile(join(folderpath,x)):
			contents.append(join(folderpath,x)[position:])
		elif isdir(join(folderpath,x)):
			folder_recurse(contents,join(folderpath,x))



def get_list_of_files_on_server():
	data = {"username":USERNAME,"password":PASSWORD}

	response = requests.post(GET_FILES_URL, data=data)
	received = response.content
	mapping = ast.literal_eval(received)
	listOfFiles = sorted(mapping.get("files"))
	return listOfFiles

def change_password():

	username = raw_input("Please enter username:")
	old_password = raw_input("Please enter your current password:")

	values = {'username': username, 'password': old_password}
	data = urllib.urlencode(values)
	req = urllib2.Request(CHECK_PASSWORD_URL, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	if str(the_page) != "true":
		print("Incorrect password.")
		main_menu2()
		return
	else:
		new_password = raw_input("Enter new password:")
		confirm = raw_input("Confirm new password:")
		while new_password != confirm:
			new_password = raw_input("Passwords do not match. Please re-enter new password:")
			confirm = raw_input("Confirm new password:")
		values = {'username': username, 'new_password': new_password}
		data = urllib.urlencode(values)
		req = urllib2.Request(CHANGE_PASSWORD_URL, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		print the_page
		main_menu2()

def signOut():
	global SYNC
	SYNC = False
	if backgroundThread.isAlive():
		backgroundThread.join()
	loginOrSignup()

def deleteFile(filepath):
	print 'deleteFile reached'
	data = {'username':USERNAME, 'password':PASSWORD, 'filepath': filepath}
	response = requests.post(DELETE_URL, data=data)


class MyHandler(FileSystemEventHandler):


	def on_created(self, event):
		print event
		global deleteThread
		if deleteThread.isAlive():
			deleteThread.join()
		if isHiddenFile(event):
			return
		
		sync()

	def on_deleted(self, event):
		print event
		global deleteThread
		if "~" in event.src_path:
			return
		if deleteThread.isAlive():
			deleteThread.join()
		if isHiddenFile(event) or event.is_directory:
			return
		position = len(ROOT)+1
		path =  event.src_path[position:]
		deleteThread = Thread(target = deleteFile, args=(path,))
		deleteThread.start()
        
	def on_modified(self, event):
		print event
		global deleteThread
		if deleteThread.isAlive():
			deleteThread.join()
		if isHiddenFile(event):
			'hidden file is true'
			return
		
		sync()
	def on_moved(self, event):
		print event
		global deleteThread
		if deleteThread.isAlive():
			deleteThread.join()
		if isHiddenFile(event):
			return
		sync()


def isHiddenFile(event):
	path = str(event.src_path)
	filename = str(path.rsplit('/',1)[1])

	if filename.startswith('.'):
		return True
	else:
		return False


def turnOnWatchdog():
	global OBSERVER
	event_handler = MyHandler()
	OBSERVER = Observer()
	OBSERVER.schedule(event_handler,path=ROOT,recursive=True)
	OBSERVER.start()
	

def turnOffWatchdog(observer):
	global OBSERVER
	observer.stop()
	observer.join()


def setUp(username,password, url):
	global USERNAME, PASSWORD, ROOT, SYNC, PULL_FILE_URL, BASE_URL, UPLOAD_URL, GET_FILES_URL, CHECK_PASSWORD_URL, CHANGE_PASSWORD_URL, DELETE_URL, CHECK_FOR_UPDATES_URL
	USERNAME = username
	PASSWORD = password
	BASE_URL = url
	ROOT =  os.path.dirname(os.path.realpath(__file__))
	UPLOAD_URL = BASE_URL + "myapp/upload/"
	GET_FILES_URL = BASE_URL + "myapp/get_list_files/"
	CHECK_PASSWORD_URL = BASE_URL + "myapp/check_password/"
	CHANGE_PASSWORD_URL = BASE_URL + "myapp/change_password/"
	CHECK_FOR_UPDATES_URL =  BASE_URL + "myapp/checkForUpdates/"
	PULL_FILE_URL = BASE_URL + "myapp/pull_file/"
	DELETE_URL = BASE_URL + "myapp/deleteFile/"
	SYNC = False
	welcome()
