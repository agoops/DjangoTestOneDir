import urllib
import urllib2
#import onedir_menu
import os
import Cookie
import datetime
import random
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



LOGIN_URL = "http://127.0.0.1:8000/myapp/login/"
SIGNUP_URL = "http://127.0.0.1:8000/myapp/signup/"
CHECK_PASSWORD_URL = "http://127.0.0.1:8000/myapp/check_password/"
CHANGE_PASSWORD_URL = "http://127.0.0.1:8000/myapp/change_password/"


def loginOrSignup():
	input = raw_input("Welcome to OneDir! Please make a selection: \n\t" \
		"[1] Login\n\t" \
		"[2] Sign up as a new user\n\t" \
		"[3] Change Password")

	try:
		selection = int(input)
	except Exception, e:
		print "Invalid input. Try again\n"
		loginOrSignup()
		return
	

	if (selection == 1):
		login_prompt()
	elif (selection == 2):
		signup_prompt()
	elif (selection == 3):
		change_password()
	else:
		print "Invalid input. Try again. \n"
		loginOrSignup()
		return


def login_prompt():

	print "\nPlease log in."
	username = raw_input("Username: ")
	password = raw_input("Password: ")

	values = {'username': username, 'password': password}
	data = urllib.urlencode(values)
	req = urllib2.Request(LOGIN_URL, data)
	code = 404
	the_page = "Page not set yet"
	try:
		response = urllib2.urlopen(req)
		code = response.getcode()
		the_page = response.read()
	except urllib2.HTTPError, err:
		print "Username or password is incorrect. Try again"
		login_prompt()
		return
	if code == 200:
		print the_page
		print "\nWelcome to Onedir!"
		#onedir_menu.main_menu()
	
		

def signup_prompt():
	print "\nPlease enter the following info to create a new account"
	username = raw_input("Username: ")
	password = raw_input("Password: ")
	retype_password = raw_input("Re-type Password: ")
	first_name = raw_input("First Name: ")
	last_name = raw_input("Last Name: ")
	email = raw_input("Email: ")

	while (password != retype_password):
		print "The passwords do not match. Please re-enter the passwords"
		password = raw_input("Password: ")
		retype_password = raw_input("Re-type Password: ")

	values = {'username': username, 'password': password, 'first_name':first_name, 'last_name': last_name, 'email': email}
	for k,v in values.iteritems():
		print k + ":\t" + v

	correct = raw_input( "Is this information correct? [y/n]")
	while (correct != "y" and correct != "n"):
		correct = raw_input( "Is this information correct? [y/n]")
	if (correct == "y"):
		data = urllib.urlencode(values)
		req = urllib2.Request(SIGNUP_URL, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		print the_page
	else: 
		signup_prompt()
		return

def change_password():

	username = raw_input("Please enter username:")
	old_password = raw_input("Please enter your current password:")

	values = {'username': username, 'password': old_password}
	data = urllib.urlencode(values)
	req = urllib2.Request(CHECK_PASSWORD_URL, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	if str(the_page) != "true":
		print str(the_page)
		print("Incorrect password. Goodbye.")
		loginOrSignup()
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
		login_prompt()

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print "Created!"
        print str(event)
        print
    def on_deleted(self, event):
        print "Deleted!"

    def on_modified(self, event):
        print "Changed!"
        print str(event)
    def on_moved(self, event):
        print "Moved!"

if __name__ == "__main__":
	loginOrSignup()
	print 'hey'
	print os.path.realpath(__file__)
	# expiration = datetime.datetime.now() + datetime.timedelta(days=30)
	# cookie = Cookie.SimpleCookie()
	# cookie["session"] = random.randint(0, 1000000000)
	# cookie["session"]["domain"] = ".jayconrod.com"
	# cookie["session"]["path"] = "/"
	# cookie["session"]["expires"] = \
 #  		expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

	# print cookie.output()
	# print
	# print "Cookie set with: " + cookie.output()
	# print
	# os.environ["HTTP_COOKIE"] = cookie.output()
	# #os.putenv("HTTP_COOKIE",cookie.output())
	# if "HTTP_COOKIE" in os.environ:
	# 	print os.environ["HTTP_COOKIE"]
	# else:
	# 	print "HTTP_COOKIE not set!"

	# while True:
	# 	x = 3
	# print
	# for k,v in os.environ.iteritems():
	# 	print 'key: ' + k + '\tvalue: ' + v + '\n'


	# event_handler = MyHandler()
	# observer = Observer()
	# observer.schedule(event_handler,path='/Users/ankitgupta/Documents/HCI/',recursive=True)
	# observer.start()
	# try:
	# 	while True:
	# 		time.sleep(1)
	# except KeyboardInterrupt:
	# 	observer.stop()
	# observer.join()










