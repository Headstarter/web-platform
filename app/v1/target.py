from app import render_template, flash
from app.router import get_locale
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from abc import ABC, abstractmethod

groups = [
    {'icon': '<img src="https://img.icons8.com/ios/50/000000/airport.png">', 'label': 'Aviation', 'tags': [0, 1, 2, 3, 4, 6, 7]},
    {'icon': 'linearicons-palette', 'label': 'Arts', 'tags': [9, 10, 12, 13]},
    {'icon': 'linearicons-store', 'label': '​Business', 'tags': [21, 22, 23, 24, 25, 26, 27, 35, 36]},
    {'icon': 'linearicons-bullhorn', 'label': 'Media', 'tags': [28, 29, 30, 31, 11, 37, 38]},
    {'icon': 'linearicons-heart-pulse', 'label': '​Medical', 'tags': [14, 15, 16, 17, 18, 19, 20]},
    {'icon': 'mercury-icon-gear', 'label': 'Service Industry', 'tags': [32, 33, 34, 5, 6]},
    {'icon': 'linearicons-graduation-hat', 'label': 'Teaching', 'tags': [32, 33, 34, 5, 6]}, 
    {'icon': 'mercury-icon-gear', 'label': 'Technology', 'tags': [32, 33, 34, 5, 6]},     
]

class Target_Group (ABC):
    
    @staticmethod
    def groupTags(company = None):
        groups1 = [
            {'id':0, 'icon': 'https://img.icons8.com/ios/50/000000/airport.png', 'label': 'Aviation', 'tags': [0, 1, 2, 3, 4, 6, 7]},
            {'id':1, 'icon': 'linearicons-palette', 'label': 'Arts', 'tags': [9, 10, 12, 13]},
            {'id':2, 'icon': 'linearicons-store', 'label': '​Business', 'tags': [21, 22, 23, 24, 25, 26, 27, 35, 36]},
            {'id':3, 'icon': 'linearicons-bullhorn', 'label': 'Media', 'tags': [28, 29, 30, 31, 11, 37, 38]},
            {'id':4, 'icon': 'linearicons-heart-pulse', 'label': '​Medical', 'tags': [14, 15, 16, 17, 18, 19, 20]},
            {'id':5, 'icon': 'mercury-icon-gear', 'label': 'Service Industry', 'tags': [32, 33, 34, 5, 6]},
            {'id':6, 'icon': 'linearicons-graduation-hat', 'label': 'Teaching', 'tags': [32, 33, 34, 5, 6]}, 
            {'id':7, 'icon': 'mercury-icon-gear', 'label': 'Technology', 'tags': [32, 33, 34, 5, 6]},    
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
            