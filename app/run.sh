python -m pip install xmlrunner requests flask flask-sqlalchemy flask_babel flask_session flask_migrate flask_script
flask db init
flask db upgrade
flask db migrate
echo -ne "from app import clear, init\nclear()\ninit()\n" | python
flask run