from app import render_template, flash
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from app.v1.target import Target_Group, abstractmethod


class Teacher:
    @staticmethod
    def folder():
        return 'visitor'

    @staticmethod
    def homepage():
        return render_template('core/' + str(session['language'] or get_locale()) + '/' + Teacher.folder() + '/index.html',
                               tags=Tag.query.all(),
                               number_offers=Position.query.filter(
                                   Position.available == True).count(),
                               open=Target_Group.groupTags(),
                               positions=Position.query.filter(
                                   Position.available == True)
                               .order_by(Position.id.desc())
                               .limit(5))
