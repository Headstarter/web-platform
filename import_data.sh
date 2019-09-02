cat regex_fix_description_problem.txt | xargs -I '{}' sed {} toimport.txt > toimport_edited.txt;
echo -e "from app.models import *\nPosition.query.filter(Position.id > 15).delete()\ndb.session.commit()\n" | CONFIG=config.cfg DEBUG=on python;
CONFIG=config.cfg DEBUG=on python import_data.py;
