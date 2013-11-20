import os
import urllib
import urllib2
import codecs
import requests
from os import listdir
from os.path import isfile, join


UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload/"


def main_menu():
	print "This is the main menu of Onedir"
	# mypath =  os.path.realpath(__file__)
	savedTextFile = codecs.open('ankitsfile.txt', 'w', 'UTF-8')

	# Add some text to it
	savedTextFile.write("line one text for example\n and line two text for example")

	rootfolder = os.path.dirname(os.path.realpath(__file__))

	onlyfiles = [ f for f in listdir(rootfolder) if isfile(join(rootfolder,f)) ]

	print
	for filex in onlyfiles:
	 	if filex.endswith(".py",0,50):
	 		print True
	 		onlyfiles.remove(filex)
	 	print filex

	print
	print

	for filex in onlyfiles:
		print filex
		fileTransfer = codecs.open(filex,'r')
		myPostRequest = requests.post(UPLOAD_URL, files={'docfile': fileTransfer})
		print str(myPostRequest)


	print "Sync complete"
	# while True:
	# 	r = raw_input("Press enter when you want to run upload stuff")
	# 	run_upload();



def run_upload():

	#Create a text file
	savedTextFile = codecs.open('tempfile.txt', 'w', 'UTF-8')

	# Add some text to it
	savedTextFile.write("line one text for example\n and line two text for example")
	fileTransfer = codecs.open('tempfile.txt','r','UTF-8')
	myPostRequest = requests.post(UPLOAD_URL, files={'docfile': fileTransfer})
	print str(myPostRequest)
	# values = {'arg':"test_argument"}
	# data = urllib.urlencode(values)
	# req = urllib2.Request(UPLOAD_URL, data)
	# code = 404
	# the_page = "Page not set yet"
	# try:
	# 	response = urllib2.urlopen(req)
	# 	code = response.getcode()
	# 	the_page = response.read()
	# except urllib2.HTTPError, err:
	# 	print "Some error occurred"
	# 	return

	# print the_page
	return 

main_menu()


#