#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

from matrix_client.api import MatrixHttpApi
from markdown2 import Markdown

from config import ICINGA_HOSTNAME, MATRIX_HOMESERVER, MATRIX_TOKEN, MATRIX_ROOM

if environ["HOSTSTATE"] == "DOWN":
    COLOR="#ff0000"
elif environ["HOSTSTATE"] == "UP":
    COLOR="#33cc33"
else:
    COLOR="#e6e6e6"

DATA = {
    "ICINGA_HOSTNAME": ICINGA_HOSTNAME,
    "COLOR": COLOR,
}
DATA.update(environ)

MSG = """**<font color="{COLOR}">Host {HOSTDISPLAYNAME} is {HOSTSTATE}</font>**

```
{HOSTOUTPUT}
```

*{LONGDATETIME} - [Show in Icinga2](https://{ICINGA_HOSTNAME}/icingaweb2/monitoring/host/show?host={HOSTNAME})* 
""".format(**DATA)

markdowner = Markdown()

matrix = MatrixHttpApi(MATRIX_HOMESERVER, token=MATRIX_TOKEN)
response = matrix.send_message_event(
    room_id=MATRIX_ROOM,
    event_type="m.room.message",
    content={
        "msgtype": "m.text",
        "format": "org.matrix.custom.html",
        "body": MSG,
        "formatted_body": markdowner.convert(MSG),
    }
)
