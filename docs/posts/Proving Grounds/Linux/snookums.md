---
title: Snookums
date: 2025-03-18
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Snookums 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250318133311.png)

The web server shows a simple PHP photo gallery `0.8`.

![](../assets/Pasted%20image%2020250318133257.png)

We find [https://www.exploit-db.com/exploits/48424](https://www.exploit-db.com/exploits/48424) that says there is a remote file inclusion.

![](../assets/Pasted%20image%2020250318185817.png)

So we can try a PHP reverse shell.

!!! bug

    Reverse shell is not connecting back, I won't lose more time on this.
