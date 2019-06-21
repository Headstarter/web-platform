from app import render_template, flash
from app.router import get_locale
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from abc import ABC, abstractmethod

groups = [
    {'icon': 'mercury-icon-globe', 'label': 'Software', 'tags': [0, 1, 2, 3, 4, 6, 7]},
    {'icon': 'mercury-icon-touch', 'label': 'Designer', 'tags': [9, 10, 12, 13]},
    {'icon': 'mercury-icon-chart-up-2', 'label': '​Sales', 'tags': [21, 22, 23, 24, 25, 26, 27, 35, 36]},
    {'icon': 'mercury-icon-partners', 'label': 'Marketing', 'tags': [28, 29, 30, 31, 11, 37, 38]},
    {'icon': 'mercury-icon-calc', 'label': '​Operations', 'tags': [14, 15, 16, 17, 18, 19, 20]},
    {'icon': 'mercury-icon-gear', 'label': 'Engineering', 'tags': [32, 33, 34, 5, 6]},    
]

class Target_Group (ABC):
    
    @staticmethod
    def groupTags(company = None):
        groups1 = [
            {'id':0, 'icon': 'mercury-icon-globe', 'label': 'Software', 'tags': [0, 1, 2, 3, 4, 6, 7]},
            {'id':1, 'icon': 'mercury-icon-touch', 'label': 'Designer', 'tags': [9, 10, 12, 13]},
            {'id':2, 'icon': 'mercury-icon-chart-up-2', 'label': '​Sales', 'tags': [21, 22, 23, 24, 25, 26, 27, 35, 36]},
            {'id':3, 'icon': 'mercury-icon-partners', 'label': 'Marketing', 'tags': [28, 29, 30, 31, 11, 37, 38]},
            {'id':4, 'icon': 'mercury-icon-calc', 'label': '​Operations', 'tags': [14, 15, 16, 17, 18, 19, 20]},
            {'id':5, 'icon': 'mercury-icon-gear', 'label': 'Engineering', 'tags': [32, 33, 34, 5, 6]},    
        ]
        
        if company == None:
            return [{'icon': x['icon'], 'id': x['id'], 'label': x['label'], 'count': sum([Position.query.filter(Position.available == True)
                                                        .filter(Position.tag_id == y)
                                                        .count() for y in x['tags']])}
                for x in groups1]
        else:
            return [{'icon': x['icon'], 'id': x['id'], 'label': x['label'], 'count': sum([Position.query.filter(Position.available == True)
                                                        .filter(Position.tag_id == y and Position.company_id == company)
                                                        .count() for y in x['tags']])}
                for x in groups1]
            