##### Utilities to check the available disk space

```
df -h

pydf

discus

di

du -hsc *

du -h | sort -h
```

##### List all running java process

```
ps -ef | grep java
```

##### Kill Process

```
kill -9 [PID]
```

#### show available RAM

```
free -h
```

##### journalctl see live log

```
journalctl -u xyz.service -f
```


##### make any user sudo user with no password permission

This will help to run sudo in shell script

```
sudo visudo -f /etc/sudoers

Enter the following line in the opened file:

jenkins ALL=(ALL) NOPASSWD: ALL

where jenkins is the user name

sudo source /etc/sudoers
```

##### convert aws pem to standard rsa key

Reference: https://stackoverflow.com/a/17734645/4439996
```
openssl rsa -in server.key -out server_new.key

openssl pkcs8 -topk8 -nocrypt -in privkey.pem
```

#### list all users

``` 
awk -F: '{ print $1}' /etc/passwd
```

