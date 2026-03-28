cd /home/52p/board
git pull



http://192.168.111.178:8000/
cd /home/gast04/board
source /home/gast04/board/venv/bin/activate
python manage.py runserver 0.0.0.0:8000