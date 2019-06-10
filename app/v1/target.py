from app import render_template, flash
from app.router import get_locale
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from abc import ABC, abstractmethod

class Target_Group (ABC):
    @staticmethod
    def groupTags():
        groups = [
            {'label': 'Software', 'tags': [0, 1, 2, 3, 4, 6, 7]},
            {'label': 'Designer', 'tags': [9, 10, 12, 13]},
            {'label': '​Operations', 'tags': [14, 15, 16, 17, 18, 19, 20]},
            {'label': '​Sales', 'tags': [21, 22, 23, 24, 25, 26, 27, 35, 36]},
            {'label': 'Marketing', 'tags': [28, 29, 30, 31, 11, 37, 38]},
            {'label': 'Engineering', 'tags': [32, 33, 34, 5, 6]},
             
        ]
        return [{'label': x['label'], 'count': sum([Position.query.filter(Position.available == True)
                                                    .filter(Position.tag_id == y)
                                                    .count() for y in x['tags']])}
               for x in groups]