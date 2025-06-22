---
title: "Hokkaido"
date: 2025-06-20
categories:
  - Proving Grounds
  - Active Directory
tags:
  - Proving Grounds
  - Active Directory
---

# Hokkaido 🔸
<!-- more -->


## Enumeration

![](../assets/Pasted%20image%2020250427110047.png)

![](../assets/Pasted%20image%2020250427110112.png)

Using `kerbrute`, discover users.

![](../assets/Pasted%20image%2020250427123246.png)

Checking `info/info`.

![](../assets/Pasted%20image%2020250427132044.png)

We find a password inside `sysvol`.

![](../assets/Pasted%20image%2020250427152444.png)
![](../assets/Pasted%20image%2020250427152454.png)

Spraying it, we find:

![](../assets/Pasted%20image%2020250427152517.png)

`discovery:Start123!`

Connect to the `db`.

![](../assets/Pasted%20image%2020250427171327.png)

Show impersonations and activate it to see the database.

![](../assets/Pasted%20image%2020250427171351.png)
![](../assets/Pasted%20image%2020250427171515.png)
![](../assets/Pasted%20image%2020250427171528.png)

So we have `hrapp-service:Untimed$Runny`

Using `bloodhound-python`, we can now see the AD.

![](../assets/Pasted%20image%2020250427172052.png)

This user has `GenericWrite` over `hazel.green`, so we can execute a targeted kerberoast from `hrapp-service`.

![](../assets/Pasted%20image%2020250427182938.png)

Using `hashcat`:

![](../assets/Pasted%20image%2020250427183043.png)

So `hazel.green:haze1988`

We can see that `hazel` belongs to `tier2-admins` and this group can `forcechangepassword` of `molly smith` who can `rdp` to the DC machine.

![](../assets/Pasted%20image%2020250427184335.png)
![](../assets/Pasted%20image%2020250427185359.png)

## Initial Access

RDP to the machine with `molly`.

![](../assets/Pasted%20image%2020250427185715.png)
![](../assets/Pasted%20image%2020250427185724.png)

Get the flag.

![](../assets/Pasted%20image%2020250427190444.png)

## Privilege Escalation

Open `powershell` as administrator.

![](../assets/Pasted%20image%2020250427203907.png)

We are `backup operator`, so get `sam` and `system` (as we are in a DC, `sam` could contain domain admin hash mirrored from `ntds.dit`).

![](../assets/Pasted%20image%2020250427205035.png)
![](../assets/Pasted%20image%2020250427205050.png)
![](../assets/Pasted%20image%2020250427205101.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250427211600.png)
