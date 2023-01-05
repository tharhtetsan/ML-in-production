


### Create SSH connection connect
##### generate RSA public key
```bash
ssh-keygen -t rsa -f tharhtetsan -C tharhtet.3@cloudsource.co.jp
```

##### connect ssh to remote server
```bash
ssh -i tharhtetsan tharhtet.3@34.171.245.255
```

##### add config in VS code
```bash
Host 34.171.245.255
  HostName 34.171.245.2
  User tharhtet.3
  IdentityFile C:\Users\tharh\tharhtet3\tharhtetsan
```



### Install docker
```bash
 sudo dpkg --configure -a
 sudo apt update
 sudo curl -sSL https://get.docker.com/ | sh

```

##### Monitor GPU

```
nvidia-smi -l 1
```

