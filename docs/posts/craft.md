---
title: "Craft"
date: 2025-06-20
categories:
  - Proving Grounds
  - Windows
tags:
  - Proving Grounds
  - Windows
---


# Craft 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250405173521.png)

We have a template page at port `80`.

![](../assets/Pasted%20image%2020250405173442.png)

There is an uploader that only accepts `.odt` files.

![](../assets/Pasted%20image%2020250406190515.png)

![](../assets/Pasted%20image%2020250405173706.png)

CMS is made with `umbraco`.

If we upload an `.odt` file, the file disappears in seconds. This is a phishing lab, it seems.

## Initial Access

Using this malicious ODT generator, we can craft an `.odt` with a macro to connect back on open.

[https://github.com/0bfxgh0st/MMG-LO](https://github.com/0bfxgh0st/MMG-LO)

![](../assets/Pasted%20image%2020250406190600.png)

Start a listener and wait.

![](../assets/Pasted%20image%2020250406190627.png)

## Privilege Escalation

Now we can put the PHP reverse shell manually in the uploads folder to pivot to the `apache` user.

![](../assets/Pasted%20image%2020250406190740.png)

![](../assets/Pasted%20image%2020250406190756.png)

Start a listener, click it, and we have a shell as `apache`.

![](../assets/Pasted%20image%2020250406190836.png)

![](../assets/Pasted%20image%2020250406190901.png)

We can impersonate, so transfer `printspoofer` and get a root shell.

![](../assets/Pasted%20image%2020250406190926.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250406190936.png)
