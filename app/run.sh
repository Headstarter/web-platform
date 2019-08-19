python -m pip install psycopg2 xmlrunner requests flask flask-sqlalchemy flask_babel flask_session flask_migrate flask_script
flask db init
flask db upgrade
flask db migrate
echo -ne "from app import clear, init\nclear()\ninit()\n" | python
flask run

https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=8672qjr3q74rgx&client_secret=AAEZwwiRpRNILccH&redirect_uri=https://headstarter.eu&scope=r_fullprofile%20r_emailaddress%20w_share&state=DCEeFWf45A53sdfKef424state=DCEeFWf45A53sdfKef424