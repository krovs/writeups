---
title: "Nagoya"
date: 2025-06-20
categories:
  - Proving Grounds
  - Active Directory
tags:
  - Proving Grounds
  - Active Directory
---

# Nagoya 🔺
<!-- more -->


## Enumeration

![](../assets/Pasted%20image%2020250425100315.png)

Web server has a landing page.

![](../assets/Pasted%20image%2020250425100410.png)

The Team tab shows all the users.

![](../assets/Pasted%20image%2020250425103804.png)

We can make a list and use `kerbrute` to check if there are valid users.

![](../assets/Pasted%20image%2020250425103842.png)

Now make a wordlist, using `2023` as the web and the image metadata is from 2023 and use seasons like `Summer`.

![](../assets/Pasted%20image%2020250425205208.png)
![](../assets/Pasted%20image%2020250425205221.png)

We have `Fiona.Clark:Summer2023` and `Craig.Carr:Spring2023`.

![](../assets/Pasted%20image%2020250425213252.png)

`SVC_HELPDESK` is kerberoastable. Having that account, we can compromise `christopher.lewis`, then connect to the machine and then `dcsync` the domain.

We can't crack `svc_helpdesk` password, but either `fiona` or `craig` have `GenericAll` over the account, so...

![](../assets/Pasted%20image%2020250426011107.png)
![](../assets/Pasted%20image%2020250426011211.png)
![](../assets/Pasted%20image%2020250426011228.png)

Now to `christopher.lewis` who can `psremote`.

![](../assets/Pasted%20image%2020250426011756.png)
![](../assets/Pasted%20image%2020250426011806.png)

## Initial Access

![](../assets/Pasted%20image%2020250426011940.png)

Get the flag.

![](../assets/Pasted%20image%2020250427010337.png)

## Privilege Escalation

`MSSQL` service is running locally, so we transfer `chisel` and make a port forward.

![](../assets/Pasted%20image%2020250427101415.png)
![](../assets/Pasted%20image%2020250427101431.png)

Now we forge a Kerberos silver ticket and connect to that port.

![](../assets/Pasted%20image%2020250427101536.png)
![](../assets/Pasted%20image%2020250427101559.png)

Transfer `printspoofer` and escalate privileges.

![](../assets/Pasted%20image%2020250427101748.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250427101910.png)
