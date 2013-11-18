import os
import urllib
import urllib2
import codecs
import requests


UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload/"


def main_menu():
	print "This is the main menu of Onedir"
	print os.path.realpath(__file__)

	while True:
		r = raw_input("Press enter when you want to run upload stuff")
		run_upload();



def run_upload():

	#Create a text file
	savedTextFile = codecs.open('ankitsfile.txt', 'w', 'UTF-8')

	# Add some text to it
	savedTextFile.write("line one texpooooooooooooooooooot for example\n and line two text for example")
	fileTransfer = codecs.open('ankitsfile.txt','r','UTF-8')
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