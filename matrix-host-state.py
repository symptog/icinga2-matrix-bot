#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

from matrix_client.api import MatrixHttpApi
from markdown2 import Markdown

from config import ICINGA_HOSTNAME, MATRIX_HOMESERVER, MATRIX_TOKEN, MATRIX_ROOM

# Format Icinag2 status to color
if environ["HOSTSTATE"] == "DOWN":
    COLOR="#ff0000"
elif environ["HOSTSTATE"] == "UP":
    COLOR="#33cc33"
else:
    COLOR="#e6e6e6"

# If notification has comment
if environ["NOTIFICATIONCOMMENT"]:
    COMMENT_PLAIN = """
Comment by {NOTIFICATIONAUTHORNAME}:
    {NOTIFICATIONCOMMENT}
""".format(**environ)
    COMMENT_MD = """>
> *Comment by {NOTIFICATIONAUTHORNAME}:*
>
> {NOTIFICATIONCOMMENT}
>""".format(**environ)
else:
    COMMENT_PLAIN = ">"
    COMMENT_MD = ">"

DATA = {
    "ICINGA_HOSTNAME": ICINGA_HOSTNAME,
    "COLOR": COLOR,
    "COMMENT_PLAIN": COMMENT_PLAIN,
    "COMMENT_MD": COMMENT_MD,
}
DATA.update(environ)

# Message without formating
MSG_PLAIN = """[{NOTIFICATIONTYPE}] Host {HOSTDISPLAYNAME} is {HOSTSTATE}

Info:   {HOSTOUTPUT}
When:   {LONGDATETIME}
{COMMENT_PLAIN}
https://{ICINGA_HOSTNAME}/icingaweb2/monitoring/host/show?host={HOSTNAME}
""".format(**DATA)

# Message in markdown
MSG_MD = """**<font color="{COLOR}">[{NOTIFICATIONTYPE}] Host {HOSTDISPLAYNAME} is {HOSTSTATE}</font>**

> *Info:*
>
> {HOSTOUTPUT}
{COMMENT_MD}
> *{LONGDATETIME} - [Show in Icinga2](https://{ICINGA_HOSTNAME}/icingaweb2/monitoring/host/show?host={HOSTNAME})*
""".format(**DATA)

# Init matrix API
matrix = MatrixHttpApi(MATRIX_HOMESERVER, token=MATRIX_TOKEN)

# Send message in both formats to channel
response = matrix.send_message_event(
    room_id=MATRIX_ROOM,
    event_type="m.room.message",
    content={
        "msgtype": "m.text",
        "format": "org.matrix.custom.html",
        "body": MSG_PLAIN,
        "formatted_body": Markdown().convert(MSG_MD),
    }
)
