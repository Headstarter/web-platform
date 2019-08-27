from app import render_template, flash
from app.router import get_locale
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from abc import ABC, abstractmethod

groups = [
    {'id':0, 'icon': 'linearicons-plane', 'label': 'Aviation', 'tags': [1,2,3,4,5,6]},
    {'id':1, 'icon': 'linearicons-palette', 'label': 'Arts', 'tags': [7,8,9,10,11,12,13]},
    {'id':2, 'icon': 'linearicons-store', 'label': '​Business', 'tags': [14,15,16,17,18,19,20,21,21,22,23,24,25]},
    {'id':3, 'icon': 'linearicons-bullhorn', 'label': 'Media', 'tags': [26,27,28,29,30,31,32]},
    {'id':4, 'icon': 'linearicons-heart-pulse', 'label': '​Medical', 'tags': [33,34,35,36,37,38,39,40,41]},
    {'id':5, 'icon': 'linearicons-store', 'label': 'Service Industry', 'tags': [42,43,44,45,46,47,48,49,50,51]},
    {'id':6, 'icon': 'linearicons-graduation-hat', 'label': 'Teaching', 'tags': [52,53,54,55,56,57]}, 
    {'id':7, 'icon': 'linearicons-cog', 'label': 'Technology', 'tags': [58,59,60,61,62,63,64,65,66,67]},    
]

class Target_Group (ABC):
    
    @staticmethod
    def groupTags(company = None):
        groups1 = [
            {'id':0, 'icon': 'linearicons-plane', 'label': 'Aviation', 'tags': [1,2,3,4,5,6]},
            {'id':1, 'icon': 'linearicons-palette', 'label': 'Arts', 'tags': [7,8,9,10,11,12,13]},
            {'id':2, 'icon': 'linearicons-store', 'label': '​Business', 'tags': [14,15,16,17,18,19,20,21,21,22,23,24,25]},
            {'id':3, 'icon': 'linearicons-bullhorn', 'label': 'Media', 'tags': [26,27,28,29,30,31,32]},
            {'id':4, 'icon': 'linearicons-heart-pulse', 'label': '​Medical', 'tags': [33,34,35,36,37,38,39,40,41]},
            {'id':5, 'icon': 'linearicons-store', 'label': 'Service Industry', 'tags': [42,43,44,45,46,47,48,49,50,51]},
            {'id':6, 'icon': 'linearicons-graduation-hat', 'label': 'Teaching', 'tags': [52,53,54,55,56,57]}, 
            {'id':7, 'icon': 'linearicons-cog', 'label': 'Technology', 'tags': [58,59,60,61,62,63,64,65,66,67]},    
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
            