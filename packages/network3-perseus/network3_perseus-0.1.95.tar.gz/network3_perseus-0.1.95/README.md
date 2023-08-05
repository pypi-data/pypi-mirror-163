# perseus
Network Device Configuration from Hedera Hashgraph Intent

## Setting up guestshell
### Enable guestshell
```console
switch# guestshell enable
```
Wait until the guestshell becomes active

### Resize guestshell diskspace
```console
switch# conf t
switch(config)# guestshell resize rootfs 2000
switch(config)# guestshell resize memory 2688
switch(config)# guesthshell reboot
```

### Update DNS
```console
[cisco@guestshell ~] $ sudo vi /etc/resolv.conf
nameserver <dns server IP address>
domain <domain that matches NX-OS configured domain>
```

## Install Python 3.8
```console
[cisco@guestshell ~] $ sudo yum -y install epel-release
[cisco@guestshell ~] $ sudo yum -y update
[cisco@guestshell ~] $ sudo yum -y groupinstall "Development Tools"
[cisco@guestshell ~] $ sudo yum -y install openssl-devel bzip2-devel libffi-devel xz-devel
```
### Confirm GCC
```console
[cisco@guestshell ~] $ gcc --version
gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39)
```
### Install Python 3.8.12
```console
[cisco@guestshell ~] $ sudo yum -y install wget
[cisco@guestshell ~] $ wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
[cisco@guestshell ~] $ tar xvf Python-3.8.12.tgz
[cisco@guestshell ~] $ cd Python-3.8*/
[cisco@guestshell ~] $ ./configure --enable-optimizations
[cisco@guestshell ~] $ sudo make altinstall
```

### Confirm install
```console
[cisco@guestshell ~]$ python3.8 --version
Python 3.8.12
[cisco@guestshell ~] $ rm -rf Python-3.8*/
[cisco@guestshell ~] $ rm Python-3.8.12.tgz
```

### Add Python to the Path

### Cleanup
```
[cisco@guestshell ~] $ rm -rf Python-3.8.12
[cisco@guestshell ~] $ rm Python-3.8.12.tgz
```

## Upgrade pip
```console
[cisco@guestshell ~] $ /usr/bin/python -m pip install --upgrade pip
```

## Install Java JDK
```console
[cisco@guestshell ~] $ curl https://download.oracle.com/java/18/latest/jdk-18_linux-x64_bin.rpm --output jdk-18_linux-x64_bin.rpm
[cisco@guestshell ~] $ sudo rpm -Uvh jdk-18_linux-x64_bin.rpm
[cisco@guestshell ~] $ cat <<EOF | sudo tee /etc/profile.d/jdk18.sh
export JAVA_HOME=/usr/java/default
export PATH=\$PATH:\$JAVA_HOME/bin
EOF
[cisco@guestshell ~] $ source /etc/profile.d/jdk18.sh
[cisco@guestshell ~] $ rm jdk-18_linux-x64_bin.rpm
```

### Verify Java
```console
[cisco@guestshell ~] $ java -version
java version "18.0.1.1" 2022-04-22
Java(TM) SE Runtime Environment (build 18.0.1.1+2-6)
Java HotSpot(TM) 64-Bit Server VM (build 18.0.1.1+2-6, mixed mode, sharing)
```

## Setup Network3 Perseus
### Install Network3_Perseus
pip install the package
```console
[cisco@guestshell ~] $ python3.8 -m pip install network3_perseus
```
### setup call_clid.py
```console
[cisco@guestshell ~] $ sudo vi call_clid.py
import sys
from cli import *

if sys.argv[1] == "show running-config":
  output = cli("show running-config")
else:
  output = clid(sys.argv[1])
print(output)  
:wq
```

### setup cli_configure.py
```console
[cisco@guestshell ~] $ sudo vi cli_configure.py
import sys
from cli import *
configuration = sys.argv[1]
cli(configuration)
:wq
```

## Configure Network3 Medusa
### Configure Java
```console
[cisco@guestshell ~] $ OPERATOR_ID={ Hedera account id }
[cisco@guestshell ~] $ OPERATOR_PRIVATE_KEY={ Hedera private key }
```

### (Optional)
Export your Webex Room and Webex token to send alerts to Webex when Network3 Medusa writes data to Hedera
export WEBEX_ROOM="Webex room id"
export WEBEX_TOKEN="Webex token id"