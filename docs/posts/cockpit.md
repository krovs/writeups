---
title: "Cockpit"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Cockpit 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250324170802.png)

Port `9090` shows the `cockpit` service page.

![](../assets/Pasted%20image%2020250324171014.png)

Port `80` shows a web page.

![](../assets/Pasted%20image%2020250324171100.png)

Using `feroxbuster` with `-x php`, we find `login.php`.

![](../assets/Pasted%20image%2020250324192352.png)

## Initial Access

And the web

![](../assets/Pasted%20image%2020250324192406.png)

It seems that there is a possible SQLi.

![](../assets/Pasted%20image%2020250324192458.png)

Putting `admin'-- -` works.

![](../assets/Pasted%20image%2020250324193553.png)

![](../assets/Pasted%20image%2020250324195254.png)

Enter and go to the terminal.

![](../assets/Pasted%20image%2020250324195432.png)

Get the flag.

## Privilege Escalation

With `sudo -l`, we see that we have permissions to run `tar` with a wildcard.

![](../assets/Pasted%20image%2020250324200330.png)

So we create in `/tmp` a checkpoint and an action to put the SUID bit on `bash`.

![](../assets/Pasted%20image%2020250324200416.png)

![](../assets/Pasted%20image%2020250324200443.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250324200510.png)
