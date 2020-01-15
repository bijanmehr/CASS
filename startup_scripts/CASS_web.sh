#!/bin/bash

sleep 10
# gnome-terminal --tab --command="/home/cabinet/Desktop/startup_web.sh ;$SHELL"
# gnome-terminal --tab --command="python3 /home/cabinet/cabinet_WebApp/manage.py runserver 0.0.0.0:8000 --noreload ;$SHELL"
# gnome-terminal -e "bash -c \"python3 /home/cabinet/cabinet_WebApp/manage.py runserver 0.0.0.0:8000 --noreload; exec bash\""
gnome-terminal -e "bash -c \"/home/cabinet/Desktop/startup_web.sh; exec bash\""