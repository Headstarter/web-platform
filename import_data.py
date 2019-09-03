# -*- coding: utf-8 -*-

import json
from app.models import *
import os
import re

lineList = list()
with open('toimport_edited.txt', 'r', encoding='utf-8') as f:
    #while True: 
    #    c = f.read(1)
    #    if not c:
    #        break
    #    print(c, end='')
    line = ''
    while True: 
        c = f.read(1)
        if not c:
            break
        if c == '\n':
            line = line.rstrip()
            if re.match(r"^  description:    '(.*)',", line): # init job line
                group, correct_group = re.match(r"^  description:    '(.*)',", line).group(1), re.match(r"^  description:    '(.*)',", line).group(1)
                correct_group = correct_group.replace('\\"', '\\\\"')
                correct_group = correct_group.replace('"', '\\"')
                correct_group = correct_group.replace("\\'", '\\"')
                correct_group = correct_group.replace('\\n', '')
                correct_group = correct_group.replace('\\t', '')
                correct_group = correct_group.replace('\\r', '')
                correct_group = correct_group.replace('\\u001f', '')
                correct_group = correct_group.replace('\\u0003', '')
                correct_group = correct_group.replace('javascript', 'Undefined')
                line = re.sub(r'%s' % re.escape(group), r'%s' % correct_group, line)
                line = re.sub(r'^  description:    \'(.*)\',', r' "description":    "\1",', line)
                lineList.append(line.rstrip())
            elif re.match(r"^.*Job [0-9]+:$", line): # init job line
                print('Starting gathering')
                line = ''
            elif re.match(r"^job [0-9]+: Generated$", line): # finialize job
                obj = {}
                flag = True
                try:
                    obj_str = ''.join(lineList)
                    obj = json.loads(obj_str)
                except Exception as e:
                    print(e, obj_str)
                    flag = False
                if flag:
                    obj['id'] = line.split(' ')[1].split(':')[0]
                    obj['views'] = '0'
                    import datetime as DT
                    obj['date'] = '{}'.format(DT.datetime.now())
                    print(obj_str)
                    print(obj)
                    offer = Position(**obj)
                    db.session.add(offer)
                    db.session.commit()
                lineList.clear()
            else:  
                line = line.rstrip()
                line = re.sub(r'^\s[\']?([A-Za-z-_]*)[\']?:', r' "\1":', line)
                line = re.sub(r': \'(.*?)\',', r': "\1",', line)
                line = re.sub(r'\'58\'', r'"58"', line)
                line = re.sub(r'\'job-title\':', r'"name":', line)
                line = re.sub(r'\'job-age\':', r'"age_required":', line)
                line = re.sub(r'\'job-type\':', r'"hours_per_day":', line)
                line = re.sub(r'\'job-category\':', r'"tag_id":', line)
                line = re.sub(r'\'job-available\':', r'"available":', line)
                line = re.sub(r'duration:', r'"duration":', line)
                line = re.sub(r'email:', r'"email":', line)
                line = re.sub(r'company_id:', r'"company_id":', line)
                line = re.sub(r'id:', r'"id":', line)
                line = re.sub(r'location:', r'"location":', line)
                line = re.sub(r'false', r'true', line)
                line = re.sub(r'""javascript:"', r'"Undefined"', line)
                lineList.append(line.rstrip())
            line = ''
        else:
            line = line + c