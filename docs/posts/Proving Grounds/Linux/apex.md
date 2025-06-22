---
title: Apex
date: 2025-03-28
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Apex 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250328134152.png)

The web server shows a page of medical stuff.

![](../assets/Pasted%20image%2020250328134243.png)

Let's add `apex.offsec` to `/etc/hosts`.

We have four potential users:

![](../assets/Pasted%20image%2020250328134432.png)

And a scheduler app:

![](../assets/Pasted%20image%2020250328134501.png)

We find documents in the `smb` share that can be accessed without a username or password.

![](../assets/Pasted%20image%2020250328134826.png)

With `feroxbuster`, we find a `filemanager` path, serving the same files as the `smb` share in a `documents` folder.

![](../assets/Pasted%20image%2020250328135236.png)

![](../assets/Pasted%20image%2020250328135300.png)

We can upload PHP files, but the app won't show them.

Searching with `searchsploit`:

![](../assets/Pasted%20image%2020250330121414.png)

We can search in GitHub where `sqlconf` is located, but we need to edit the script and put `Documents` in the path where the file is being copied to. This way, we can see it in the `smb` share, since here we can't see PHP files.

![](../assets/Pasted%20image%2020250330121051.png)

![](../assets/Pasted%20image%2020250330121103.png)

![](../assets/Pasted%20image%2020250330121115.png)

## Initial Access

We can access the database with the credentials and get users.

![](../assets/Pasted%20image%2020250330121142.png)

![](../assets/Pasted%20image%2020250330121159.png)

![](../assets/Pasted%20image%2020250330121208.png)

Using `searchsploit` to get an `openemr` exploit:

![](../assets/Pasted%20image%2020250330121323.png)

![](../assets/Pasted%20image%2020250330121251.png)

![](../assets/Pasted%20image%2020250330121454.png)

## Privilege Escalation

The password is the same as before.

![](../assets/Pasted%20image%2020250330121512.png)

## Post Exploitation

Get the flag:

![](../assets/Pasted%20image%2020250330121713.png)
