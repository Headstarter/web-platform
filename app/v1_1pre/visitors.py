from app import render_template, flash
from app.router import session
from flask import request, redirect
from app.models import User, Company, Position, Tag, Application, insert_application


class Visitors:

    @staticmethod
    def homepage():
        return render_template('visitor/homepage.html',
                               positions=Position.query.filter(Position.available==True).order_by(
                                         Position.id.desc()).limit(5),
                               companies=Company.query.all())


    @staticmethod
    def apply_student(position_id):
        if session['type'] != 'Student':
            session['redirect'] = request.full_path
            return redirect('/login/student')
        else:
            #flash(position_id, 'info')
            #flash(len(Position.query.filter(id==position_id).all()), 'info')
            #flash(Position.query.filter(id==int(position_id)).all(), 'info')
            position_id = int(position_id)
            insert_application(session['id'], position_id, Position.query.filter(Position.id==position_id).one().company_id);
            flash('Кандидатстването Ви беше успешно.<style>.formater { background: transparent !important; }</style>', 'success')
            return render_template('template.html')


    @staticmethod
    def browse_offers():
        page = int(request.args.get('page', default='0'))
        offers_per_page = 10
        position = -1
        if request.form.get('position'):
            position = int(request.form.get('position')) - 1

        if position == -1:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 0:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id < 9)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 10:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id > 8)
                                   .filter(Position.tag_id < 14)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 14:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id > 13)
                                   .filter(Position.tag_id < 21)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 21:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id > 21)
                                   .filter(Position.tag_id < 28)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 28:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id > 28)
                                   .filter(Position.tag_id < 32)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())

        elif position == 39:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id > 39)
                                   .limit(offers_per_page)
                                   .offset(page * offers_per_page),
                                   tags=Tag.query.filter(True).all())
        else:
            return render_template('visitor/browse.html',
                                   positions=Position.query.filter(Position.available == True)
                                   .filter(Position.tag_id == position + 1),
                                   tags=Tag.query.filter(True).all())

    @staticmethod
    def all_positions():
        return render_template('visitor/positions.html',
                               positions=Position.query.filter(Position.available==True))
