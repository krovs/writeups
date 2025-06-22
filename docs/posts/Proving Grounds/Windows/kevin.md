---
title: Kevin
date: 2025-03-02
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Kevin 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250302232008.png)

The web server at port `80` welcomes us with a login form. Trying `admin:admin` hits the jackpot.

![](../assets/Pasted%20image%2020250302232655.png)
![](../assets/Pasted%20image%2020250302232807.png)

This is an `HP Power Manager 4.2 (Build 7)`.

## Initial Access

Use this exploit: [https://github.com/Muhammd/HP-Power-Manager/blob/master/hpm_exploit.py](https://github.com/Muhammd/HP-Power-Manager/blob/master/hpm_exploit.py)

Execute it with the machine IP.

![](../assets/Pasted%20image%2020250302234049.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250302234203.png)
