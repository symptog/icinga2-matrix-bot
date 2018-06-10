# Icinga2 Matrix Bot

System requirements:

  * python-virtualenv

Matrix requirements:

  * Matrix User
  * Matrix User API-Token
  * Matrix Room ID (starting with `!`)

## Installation

```
$ cd /opt 
$ git clone https://github.com/symptog/icinga2-matrix-bot.git
$ cd icinga2-matrix-bot
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Setup Icinga2

**This steps may depend on you Icinga2 setup**

  * Copy `icinga2/matrix-host-notification.sh` to `/etc/icinga2/scripts/`
    * In the file: change the path of the `.venv`
  * Copy `icinga2/matrix-service-notification.sh` to `/etc/icinga2/scripts/`
    * In the file: change the path of the `.venv`
  * Add the contents of `icinga2/matrix-commands.conf` to `/etc/icinga2/conf.d/commands.conf`
  * Add the contents of `icinga2/matrix-notifications.conf` to `/etc/icinga2/conf.d/notifications.conf`
  * Add the contents of `icinga2/matrix-templates.conf` to `/etc/icinga2/conf.d/templates.conf`
  * Add the contents of `icinga2/matrix-users.conf` to `/etc/icinga2/conf.d/users.conf`
  * Add the following to your host objects:
    ```
    vars.notification["matrix"] = {
      groups = [ "matrix" ]
    }
    ```


