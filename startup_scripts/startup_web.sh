
#!/bin/bash

# if pidof -x "abc.sh" >/dev/null; then
#     # echo "Process already running"
#     echo "start CASS"
#     echo "start web app"
#     python3 /home/cabinet/cabinet_WebApp/manage.py runserver 0.0.0.0:8000 --noreload
# else
#     /home/cabinet/Desktop/startup_web.sh
# fi

echo "start CASS"
echo "start web app"
source /home/cabinet/catkin_ws/devel/setup.bash
python3 /home/cabinet/cabinet_WebApp/setip.py --src /home/cabinet/cabinet_WebApp/website/frontend/build --address 192.168.0.100:8000
sleep 2
python3 /home/cabinet/cabinet_WebApp/manage.py runserver 192.168.0.100:8000 --noreload