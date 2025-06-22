---
title: Marketing
date: 2025-04-02
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Marketing 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250402124233.png)

Web server is a marketing page.

![](../assets/Pasted%20image%2020250402124539.png)

Using `feroxbuster`, we find `/old` path.

![](../assets/Pasted%20image%2020250402170930.png)

Inside the old index, there is a new link.

![](../assets/Pasted%20image%2020250402170950.png)

![](../assets/Pasted%20image%2020250402171004.png)

Add this to `/etc/hosts` and access it.

![](../assets/Pasted%20image%2020250403175009.png)

Going to `/admin`.

![](../assets/Pasted%20image%2020250403183405.png)

Searching default credentials.

![](../assets/Pasted%20image%2020250403184132.png)

## Initial Access

![](../assets/Pasted%20image%2020250403184151.png)

We are in.

Using this exploit [https://github.com/Y1LD1R1M-1337/Limesurvey-RCE](https://github.com/Y1LD1R1M-1337/Limesurvey-RCE) (recreate the zip after editing the reverse shell).

![](../assets/Pasted%20image%2020250403195126.png)

![](../assets/Pasted%20image%2020250403195142.png)

## Privilege Escalation

Limesurvey config files show SQL credentials.

![](../assets/Pasted%20image%2020250403195537.png)

![](../assets/Pasted%20image%2020250403202019.png)

`sync.sh`

![](../assets/Pasted%20image%2020250403203915.png)

Testing MySQL password with `t.miller` is a go.

![](../assets/Pasted%20image%2020250403205358.png)

Get the flag.

![](../assets/Pasted%20image%2020250403205416.png)

With `t.miller` we can execute `/usr/bin/sync.sh`.

![](../assets/Pasted%20image%2020250403205733.png)

`t.miller` is a `staff` user and `mlocate` user.

Transfer the database to Kali and inspect it, searching for the personal folder.

![](../assets/Pasted%20image%2020250403220754.png)

So we have to read `creds-for-2022.txt` but if we pass the path to the program, it is going to fail because of the...

![](../assets/Pasted%20image%2020250403221130.png)

...part, so we can disguise it with a symbolic link.

![](../assets/Pasted%20image%2020250403221708.png)

![](../assets/Pasted%20image%2020250403222556.png)

![](../assets/Pasted%20image%2020250403222731.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250403222742.png)
