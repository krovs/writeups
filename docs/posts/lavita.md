---
title: "Lavita"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Lavita 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250410234932.png)

Page shows a template.

![](../assets/Pasted%20image%2020250410235053.png)

`feroxbuster` finds a `register` path.

![](../assets/Pasted%20image%2020250410235155.png)

We can create an account and...

![](../assets/Pasted%20image%2020250410235233.png)

![](../assets/Pasted%20image%2020250410235808.png)

## Initial Access

Searching exploits for `laravel` and `debug`, we find [https://github.com/rocketscientist911/CVE-2021-3129](https://github.com/rocketscientist911/CVE-2021-3129).

We need to clone [https://github.com/ambionics/phpggc.git](https://github.com/ambionics/phpggc.git) to the same folder as the `.py` file and edit the exploit with the URL and the payload.

![](../assets/Pasted%20image%2020250411003730.png)

![](../assets/Pasted%20image%2020250411003741.png)

Get the flag.

![](../assets/Pasted%20image%2020250411003927.png)

## Privilege Escalation

![](../assets/Pasted%20image%2020250411004756.png)

Using `pspy64`, we notice a task with the user `skunk` that uses `artisan`.

![](../assets/Pasted%20image%2020250411012923.png)

So we replace `artisan` with a PHP reverse shell.

![](../assets/Pasted%20image%2020250411012945.png)

Now using `sudo -l`...

![](../assets/Pasted%20image%2020250411013800.png)

This user can execute `composer` in that specific path, so reading on `gtfobins`...

![](../assets/Pasted%20image%2020250411013829.png)

I'll use the first user `www-data` to put the payload in the `composer.json`.

![](../assets/Pasted%20image%2020250411013915.png)

And now execute `composer` with `skunk`.

![](../assets/Pasted%20image%2020250411013944.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250411013954.png)
