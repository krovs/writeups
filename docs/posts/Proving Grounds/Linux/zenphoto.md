---
title: Zenphoto
date: 2025-03-21
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Zenphoto 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250322013421.png)

The webpage is under construction.

![](../assets/Pasted%20image%2020250322013442.png)

We find a `test` folder with `feroxbuster`.

![](../assets/Pasted%20image%2020250322013617.png)

And the `robots.txt`.

![](../assets/Pasted%20image%2020250322013657.png)

The test root is the gallery.

![](../assets/Pasted%20image%2020250322014034.png)

And we have admin access.

![](../assets/Pasted%20image%2020250322014049.png)

If we look at the source code, we get the version.

![](../assets/Pasted%20image%2020250322015355.png)

## Initial Access

![](../assets/Pasted%20image%2020250322015415.png)

Fixing the PHP script.

![](../assets/Pasted%20image%2020250322021041.png)

Get the flag.

![](../assets/Pasted%20image%2020250322021305.png)

## Privilege Escalation

Get a more stable shell with `python`.

![](../assets/Pasted%20image%2020250322025237.png)

Transfer `linpeas`.

![](../assets/Pasted%20image%2020250322025420.png)

Using `rds` one:

[https://www.exploit-db.com/exploits/15285](https://www.exploit-db.com/exploits/15285)

![](../assets/Pasted%20image%2020250322025953.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250322030027.png)
