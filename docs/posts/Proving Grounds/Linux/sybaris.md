---
title: Sybaris
date: 2025-03-30
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Sybaris 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250330170303.png)

The web server has a PHP blog.

![](../assets/Pasted%20image%2020250330170412.png)

![](../assets/Pasted%20image%2020250330170539.png)

The blog is made with `htmly` and Pablo.

![](../assets/Pasted%20image%2020250330170930.png)

`ftp` shows an exit pub folder.

Using `redis-cli`, we can connect; it is open.

We can upload a Redis module to execute system commands. Upload it to the `ftp` server and load it with `redis`.

[https://book.hacktricks.wiki/en/network-services-pentesting/6379-pentesting-redis.html#load-redis-module](https://book.hacktricks.wiki/en/network-services-pentesting/6379-pentesting-redis.html#load-redis-module)  
[https://github.com/n0b0dyCN/RedisModules-ExecuteCommand#](https://github.com/n0b0dyCN/RedisModules-ExecuteCommand#)

![](../assets/Pasted%20image%2020250330204047.png)

![](../assets/Pasted%20image%2020250330210000.png)

Load the module from the default public `vftpd`.

![](../assets/Pasted%20image%2020250330210034.png)

Execute a reverse shell.

![](../assets/Pasted%20image%2020250330204226.png)

![](../assets/Pasted%20image%2020250330204313.png)

Get the flag.

![](../assets/Pasted%20image%2020250330221230.png)

## Privilege Escalation

Searching for passwords in the blog project, we find Pablo's.

![](../assets/Pasted%20image%2020250330221107.png)

It is better to connect via `ssh`.

Transfer `linpeas`.

![](../assets/Pasted%20image%2020250330222017.png)

![](../assets/Pasted%20image%2020250330222124.png)

Compile a shared object with malicious code and put it in `/usr/local/lib/dev` and wait.

![](../assets/Pasted%20image%2020250330233851.png)

![](../assets/Pasted%20image%2020250330233929.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250330233942.png)
