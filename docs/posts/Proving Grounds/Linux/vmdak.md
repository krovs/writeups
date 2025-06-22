---
title: "Vmdak"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Vmdak 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250423233807.png)

`ftp` has anonymous access with a Jenkins file.

![](../assets/Pasted%20image%2020250424020424.png)

Web server shows a prison management system.

![](../assets/Pasted%20image%2020250423234522.png)

## Initial Access

Searching for an exploit, we have an SQL injection.

![](../assets/Pasted%20image%2020250423235208.png)

![](../assets/Pasted%20image%2020250423235136.png)

![](../assets/Pasted%20image%2020250423235220.png)

Inside, there is a user with a password:

![](../assets/Pasted%20image%2020250423235327.png)

`malcom:RonnyCache001`

And the admin credentials.

![](../assets/Pasted%20image%2020250424000033.png)

Now we can upload a PHP reverse shell using the avatar uploader, bypassing the jpg extension like `.jpg.php`.

![](../assets/Pasted%20image%2020250424013942.png)

![](../assets/Pasted%20image%2020250424013850.png)

## Privilege Escalation

We see that there is a user we can pivot to: `vmdak`.

![](../assets/Pasted%20image%2020250424014210.png)

Let's try the password from `malcom`.

![](../assets/Pasted%20image%2020250424014232.png)

Get the flag.

![](../assets/Pasted%20image%2020250424014320.png)

We can connect via `ssh` with `vmdak` and stabilize the shell with `python` to have a fully interactive shell.

![](../assets/Pasted%20image%2020250424014626.png)

Prison web has SQL credentials.

![](../assets/Pasted%20image%2020250424022625.png)

`sqlCr3ds3xp0seD`

We have Jenkins at port `8080` and MySQL at `3306`.

In the `3306` database, we have `malcom` data.

![](../assets/Pasted%20image%2020250424022914.png)

For Jenkins, transfer `chisel` to the target and make a port forward.

![](../assets/Pasted%20image%2020250424171451.png)

![](../assets/Pasted%20image%2020250424171456.png)

Jenkins is protected with a password.

![](../assets/Pasted%20image%2020250424171609.png)

Searching Jenkins exploits, we find an LFI.

![](../assets/Pasted%20image%2020250424171429.png)

Run the script with the path for Jenkins.

![](../assets/Pasted%20image%2020250424171507.png)

Now we can enter.

![](../assets/Pasted%20image%2020250424171900.png)

Create a job that puts the SUID bit on `/bin/bash`.

![](../assets/Pasted%20image%2020250424172121.png)

Build.

![](../assets/Pasted%20image%2020250424172151.png)

Let's check.

![](../assets/Pasted%20image%2020250424172303.png)

So:

![](../assets/Pasted%20image%2020250424172312.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250424172322.png)
