# Docker Installation and Configuration

**Note**:

## Installation

### Set up the repository

1. Update the `apt` package index and install packages to allow `apt` to use a repository over HTTPS:

```terminal
user@server:~$ sudo apt-get update
user@server:~$ sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

2. Add Docker’s official GPG key:

```terminal
user@server:~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

3. Use the following command to set up the stable repository.

```terminal
user@server:~$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
```

### Install Docker Engine

1. Update the `apt` package index, and install the latest version of Docker Engine, containerd, and Docker Compose:

```terminal
user@server:~$ sudo apt-get update
user@server:~$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### Install Docker-Compose

1. Download the lastest version of docker-compose

```terminal
user@server:~$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

2. Give Permissions to the exec file

```terminal
user@server:~$ sudo chmod +x /usr/local/bin/docker-compose
```

3. Check if it installed

```terminal
user@server:~$ docker-compose --version
docker-compose version 1.29.1, build c34c88b2
```

## Configuration

1. Create the project folder

```terminal
root@server:~$ sudo mkdir -p /opt/develop/app/
root@server:~$ cd /opt/develop/app/
```

2. Clone the repository

3. Set the .env vars

4. Run the project

```terminal
user@server:~/opt/develop/app/$ docker-compose -f docker-compose.prod.yml up -d --build
```
