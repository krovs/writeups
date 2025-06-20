---
title: "Quackerjack"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Quackerjack 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250404165200.png)

At port `8081` we have an `rconfig` service.

Searching for an exploit, we find:

![](../assets/Pasted%20image%2020250404175120.png)

## Initial Access

The problem is that the final step, the execution of the reverse shell, is not working.

![](../assets/Pasted%20image%2020250404175148.png)

So we are going to use the created user and use another exploit from the inside.

[https://gist.github.com/FlatL1neAPT/c2a339ca76d0db05a281f2e6e77ad56c](https://gist.github.com/FlatL1neAPT/c2a339ca76d0db05a281f2e6e77ad56c)

So upload in `vendors` a `shell.php`, capture the request with `caido` and put `image/gif` in content-type, then go to `/images/vendor/shell.php` to get a reverse shell.

![](../assets/Pasted%20image%2020250404175328.png)

![](../assets/Pasted%20image%2020250404175338.png)

![](../assets/Pasted%20image%2020250404175348.png)

Get the flag.

![](../assets/Pasted%20image%2020250404182554.png)

## Privilege Escalation

Get credentials.

![](../assets/Pasted%20image%2020250404182938.png)

Inside `mysql` we have the `admin` user.

![](../assets/Pasted%20image%2020250404183132.png)

Using `hashcat`.

![](../assets/Pasted%20image%2020250404183231.png)

Looking for SUID, we find:

![](../assets/Pasted%20image%2020250404183635.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250404183647.png)
