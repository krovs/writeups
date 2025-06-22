---
title: "Astronaut"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Astronaut 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250402000746.png)

The web server has a file index with a `grav` page inside.

![](../assets/Pasted%20image%2020250402000948.png)

![](../assets/Pasted%20image%2020250402001020.png)

## Initial Access

Using this exploit [`exploit.py`](https://github.com/CsEnox/CVE-2021-21425/blob/main/exploit.py), we can get a shell.

![](../assets/Pasted%20image%2020250402003341.png)

## Privilege Escalation

We have `php` with the SUID bit set.

![](../assets/Pasted%20image%2020250402004539.png)

![](../assets/Pasted%20image%2020250402004518.png)

## Post Exploitation

Get the flag:

![](../assets/Pasted%20image%2020250402004603.png)
