import urllib
import urllib2
import onedir_menu
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
	print "\n\n**********************************************************************\n\n"
	input = raw_input("Welcome to OneDir! Please make a selection: \n\t" \
		"[1] Login\n\t" \
		"[2] Sign up as a new user\n\t" \
		"[3] Quit")

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
		quit()
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
		onedir_menu.setUp(username,password)
	
		

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


if __name__ == "__main__":
	loginOrSignup()










