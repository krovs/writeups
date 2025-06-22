---
title: "Authby"
date: 2025-06-20
categories:
  - Proving Grounds
  - Windows
tags:
  - Proving Grounds
  - Windows
---


# Authby 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250411235902.png)

Enumerating the `ftp`, we can log in as `anonymous`.

![](../assets/Pasted%20image%2020250412004556.png)
![](../assets/Pasted%20image%2020250412004608.png)

We can notice `offsec`, `anonymous`, and `admin` that can be users.

We try to re-login with `admin:admin` and it works.

![](../assets/Pasted%20image%2020250412004904.png)
![](../assets/Pasted%20image%2020250412005146.png)

## Initial Access

We have credentials for port `242`.

Using `john`...

![](../assets/Pasted%20image%2020250412005254.png)

We can write to that `ftp` folder, so now we can upload a reverse shell and...

![](../assets/Pasted%20image%2020250412005953.png)
![](../assets/Pasted%20image%2020250412010003.png)

## Privilege Escalation

Get the flag.

![](../assets/Pasted%20image%2020250412010132.png)

We have `SeImpersonatePrivilege`.

![](../assets/Pasted%20image%2020250412015027.png)

But this is an old machine x86 and we need `juicy potato x86` and a correct `CLSID`.

[https://github.com/ivanitlearning/Juicy-Potato-x86](https://github.com/ivanitlearning/Juicy-Potato-x86)

[https://github.com/ohpe/juicy-potato/tree/master/CLSID/Windows_Server_2008_R2_Enterprise](https://github.com/ohpe/juicy-potato/tree/master/CLSID/Windows_Server_2008_R2_Enterprise)

So transfer `potato` and a reverse shell with `msfvenom x86`.

![](../assets/Pasted%20image%2020250412015250.png)
![](../assets/Pasted%20image%2020250412015312.png)
![](../assets/Pasted%20image%2020250412015324.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250412015333.png)

## Another Privilege Escalation (intended)

This is a very old machine, search for a privilege escalation exploit.

![](../assets/Pasted%20image%2020250412015810.png)

Compile it, transfer it, and execute it.
