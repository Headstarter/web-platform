# -*- coding: utf-8 -*-

import json

import sys
sys.path.append("..")
sys.path.append(".")

from app.models import *
import os
import re
try:
    companies = open('companies.txt', 'r', encoding='utf-8')
    line = companies.readline()
    while line:
        company = json.loads(line)
        company.pop('index', None)
        company.pop('offers', None)
        company['name'] = company['name']
        try:
            db.session.add(Company(**company))
            db.session.commit()
        except Exception as e:
            print('ROLLBACK:', company['id'], company['name'])
            print('  REASON:', e)
            db.session.rollback()
        line = companies.readline()
    companies.close()
except Exception as e:
    print(e)
    
try:
    jobs = open('jobs.txt', 'r', encoding='utf-8')
    line = jobs.readline()
    while line:
        job = json.loads(line)
        job['name'] = job['name'][3:-4]
        job['description'] = job['description'].replace('/htmltemplates/', 'https://www.jobs.bg/htmltemplates/')
        try:
            db.session.add(Position(**job))
            db.session.commit()
        except Exception as e:
            print('ROLLBACK:', job['id'], job['name'])
            print('  REASON:', e)
            db.session.rollback()
        line = jobs.readline()
    jobs.close()
except Exception as e:
    print(e)