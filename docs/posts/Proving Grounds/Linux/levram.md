---
title: "Levram"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Levram 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250409125010.png)

At port `800` we have a login page for `gerapy`.

![](../assets/Pasted%20image%2020250409125439.png)

Testing `admin:admin` works.

## Initial Access

`searchsploit` gives us the exploit for `gerapy`.

![](../assets/Pasted%20image%2020250409132207.png)

Create a project in the app and execute the script.

![](../assets/Pasted%20image%2020250409132302.png)

Get the flag.

![](../assets/Pasted%20image%2020250409132347.png)

## Privilege Escalation

Transfer `linpeas`.

![](../assets/Pasted%20image%2020250409134755.png)

`python` has capabilities so:

![](../assets/Pasted%20image%2020250409134814.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250409134825.png)
