---
title: "Sorcerer"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Sorcerer 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250330123225.png)

![](../assets/Pasted%20image%2020250330123232.png)

The web server shows a 404 not found. Let's try `feroxbuster`.

Port `7742` shows a login form, but it is not working; the front always shows invalid login.

![](../assets/Pasted%20image%2020250330125803.png)

![](../assets/Pasted%20image%2020250330125819.png)

`feroxbuster` finds a `zipfiles` path.

![](../assets/Pasted%20image%2020250330123713.png)

We find an `id_rsa` key in Max's zip.

![](../assets/Pasted%20image%2020250330124108.png)

We also find a Tomcat password.

![](../assets/Pasted%20image%2020250330131824.png)

A wrapper prevents SSH access, only `scp`.

![](../assets/Pasted%20image%2020250330162325.png)

## Initial Access

The authorized keys use this wrapper, so we can remove it and `scp` it to replace it, and connect with SSH normally.

![](../assets/Pasted%20image%2020250330162501.png)

![](../assets/Pasted%20image%2020250330162558.png)

![](../assets/Pasted%20image%2020250330162524.png)

## Privilege Escalation

Get the flag.

![](../assets/Pasted%20image%2020250330164953.png)

![](../assets/Pasted%20image%2020250330164725.png)

![](../assets/Pasted%20image%2020250330164750.png)

![](../assets/Pasted%20image%2020250330164800.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250330164808.png)
