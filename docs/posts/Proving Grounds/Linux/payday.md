---
title: "Payday"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Payday 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250317192645.png)

The web page is...

![](../assets/Pasted%20image%2020250317192943.png)

## Initial Access

We can log in with `admin:admin`.

Using `feroxbuster`, we discover `/admin` and using `admin:admin` we are inside.

![](../assets/Pasted%20image%2020250317193602.png)

Go to template editor and upload a PHP reverse shell with `.phtml` as seen in...

![](../assets/Pasted%20image%2020250317194757.png)

Once uploaded, go to `http://[victim]/skins/shell.phtml` after setting a reverse shell.

![](../assets/Pasted%20image%2020250317194950.png)

## Privilege Escalation

Get `local.txt`.

![](../assets/Pasted%20image%2020250317195318.png)

Enumerating users, we see `patrick` and testing `patrick` with password `patrick`.

![](../assets/Pasted%20image%2020250317210147.png)

And `patrick` has all privileges.

![](../assets/Pasted%20image%2020250317210236.png)

![](../assets/Pasted%20image%2020250317210249.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250317210324.png)
