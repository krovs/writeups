---
title: "Hetemit"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Hetemit 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250320001715.png)
![](../assets/Pasted%20image%2020250320001735.png)

## Initial Access

Going to port `50000`, we have a Python API that shows...

![](../assets/Pasted%20image%2020250320102701.png)

At `/verify` we can inject code using `os.system()` because it is Python.

Using `caido`.

![](../assets/Pasted%20image%2020250320102743.png)

![](../assets/Pasted%20image%2020250320102807.png)

Get the flag.

![](../assets/Pasted%20image%2020250320102902.png)

## Privilege Escalation

Checking with `linpeas`.

![](../assets/Pasted%20image%2020250320123728.png)

![](../assets/Pasted%20image%2020250320123743.png)

We can reboot the system and write to that service.

![](../assets/Pasted%20image%2020250320124125.png)

It's impossible to edit the file without a fully interactive shell, so let's use `penelope`.

[https://github.com/brightio/penelope](https://github.com/brightio/penelope)

![](../assets/Pasted%20image%2020250320130850.png)

Change the execution and the user.

![](../assets/Pasted%20image%2020250320132936.png)

We reboot and wait.

`sudo /sbin/reboot`

![](../assets/Pasted%20image%2020250320133034.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250320133104.png)
