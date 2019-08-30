import json
from app.models import *

lineList = list()
with open('toimport.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.find('Job') != -1: # init job line
            pass
        elif line.startswith('job'): # finialize job
            obj = {}
            try:
                import re
                obj_str = ''.join(lineList)
                obj_str = re.sub(r'"javascript:', r'Undefined', obj_str)
                obj_str = re.sub(r' [\']?([a-z-_]*)[\']?:', r' "\1":', obj_str)
                obj_str = re.sub(r': \'(.*?)\',', r': "\1",', obj_str)
                obj_str = re.sub(r'\'58\'', r'"58"', obj_str)
                obj_str = re.sub(r'"description":  ', r'"description":  "",', obj_str)
                obj_str = re.sub(r'job-title', r'name', obj_str)
                obj_str = re.sub(r'job-age', r'age_required', obj_str)
                obj_str = re.sub(r'job-type', r'hours_per_day', obj_str)
                obj_str = re.sub(r'job-category', r'tag_id', obj_str)
                obj_str = re.sub(r'job-available', r'available', obj_str)
                obj_str = re.sub(r'false', r'true', obj_str)
                           
                obj = json.loads(obj_str)
            except Exception as e:
                print(e, obj_str)
                break
            obj['id'] = line.split(' ')[1].split(':')[0]
            obj['views'] = '0'
            import datetime as DT
            obj['date'] = '{}'.format(DT.datetime.now())
            print(obj)
            offer = Position(**obj)
            db.session.add(offer)
            db.session.commit()
            lineList.clear()
        else:
            lineList.append(line.rstrip())