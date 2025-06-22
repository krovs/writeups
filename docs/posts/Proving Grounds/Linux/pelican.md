---
title: Pelican
date: 2025-03-13
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Pelican 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250313233355.png)

![](../assets/Pasted%20image%2020250313233506.png)

We see an exhibitor for `zookeeper` on port `8080`.

![](../assets/Pasted%20image%2020250313235306.png)

## Initial Access

Searching, we have:

![](../assets/Pasted%20image%2020250313235326.png)

So adding a `nc` in the correct field.

![](../assets/Pasted%20image%2020250313235406.png)

We have access.

![](../assets/Pasted%20image%2020250313235427.png)

Get the flag.

![](../assets/Pasted%20image%2020250313235441.png)

## Privilege Escalation

With `sudo -l` we can see `gcore` privileges.

![](../assets/Pasted%20image%2020250314002203.png)

![](../assets/Pasted%20image%2020250314002230.png)

With `ps aux` we search for a process with password and see `password store`.

![](../assets/Pasted%20image%2020250314002331.png)

So using that PID, and then using `strings` on the file, we have a password.

![](../assets/Pasted%20image%2020250314002431.png)

Now we can execute commands as `root` (I couldn't switch to the user; next time use a bash connection instead of `nc`).

![](../assets/Pasted%20image%2020250314002512.png)

![](../assets/Pasted%20image%2020250314002539.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250314002600.png)
