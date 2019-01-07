python -m pip install flask flask-sqlalchemy flask_babel
flask db init
flask db migrate
flask db upgrade
echo -ne "from app import clear, init\nclear()\ninit()\n" | python
flask run