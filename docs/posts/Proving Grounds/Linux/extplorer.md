---
title: "Extplorer"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Extplorer 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250325123844.png)

The web server has a brand new `WordPress` without any configuration. Using `feroxbuster`, we find `/filemanager/index.php`.

![](../assets/Pasted%20image%2020250325124649.png)

Testing `admin:admin`, we get inside.

![](../assets/Pasted%20image%2020250325124724.png)

We find a user `dora`.

![](../assets/Pasted%20image%2020250325124853.png)

And the version.

![](../assets/Pasted%20image%2020250325124908.png)

## Initial Access

Upload a PHP reverse shell to `/wordpress`.

![](../assets/Pasted%20image%2020250325125904.png)

And we are in as `www-data`.

![](../assets/Pasted%20image%2020250325125929.png)

## Privilege Escalation

Looking at the files, we find:

![](../assets/Pasted%20image%2020250325135148.png)

And using `hashcat`:

![](../assets/Pasted%20image%2020250325135203.png)

So we can pivot to `dora`.

![](../assets/Pasted%20image%2020250325135237.png)

Then the flag.

![](../assets/Pasted%20image%2020250325135413.png)

`dora` belongs to the `disk` group.

![](../assets/Pasted%20image%2020250325140954.png)

So we can read root files using `debugfs`.

![](../assets/Pasted%20image%2020250325141038.png)

Getting `shadow` and `passwd`.

![](../assets/Pasted%20image%2020250325141111.png)

Using:

![](../assets/Pasted%20image%2020250325141126.png)

And `john`:

![](../assets/Pasted%20image%2020250325141140.png)

We have the password: `explorer`.

![](../assets/Pasted%20image%2020250325141159.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250325141215.png)
