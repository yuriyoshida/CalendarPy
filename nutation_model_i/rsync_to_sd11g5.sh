#!/bin/bash

APP=calendar_py/nutation_model
USER=masaru
SERVER=sd11g5
PORT=3701
EXCLUDE=./rsync_exclude.lst
OPTIONS="-auv --no-p --no-o --no-g --delete"

rsync $OPTIONS --exclude-from=$EXCLUDE -e "ssh -p $PORT" /home/$USER/src/$APP/ $USER@$SERVER:~/src/$APP

