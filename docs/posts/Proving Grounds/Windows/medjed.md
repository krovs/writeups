---
title: Medjed
date: 2025-04-08
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Medjed 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250408233009.png)

Port `33033` has a simple page with a login form.

![](../assets/Pasted%20image%2020250408233342.png)
![](../assets/Pasted%20image%2020250408233352.png)

We have a `barracuda` service at port `8000`.

![](../assets/Pasted%20image%2020250408232547.png)

Set the account.

## Initial Access

Using `cadaver`, we can use `webdav` with the account and upload a PHP reverse shell to `xampp\htdocs`.

![](../assets/Pasted%20image%2020250409010423.png)
![](../assets/Pasted%20image%2020250409010434.png)
![](../assets/Pasted%20image%2020250409010448.png)

Get the flag.

![](../assets/Pasted%20image%2020250409010537.png)

## Privilege Escalation

`winpeas` found `jerren` password.

![](../assets/Pasted%20image%2020250409005144.png)
![](../assets/Pasted%20image%2020250409012917.png)

We can write the exe of an autorun app, so replace it with a shell and restart.

![](../assets/Pasted%20image%2020250409013758.png)
![](../assets/Pasted%20image%2020250409013733.png)
![](../assets/Pasted%20image%2020250409013745.png)
![](../assets/Pasted%20image%2020250409013659.png)
![](../assets/Pasted%20image%2020250409013708.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250409013716.png)
