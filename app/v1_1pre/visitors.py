from app import render_template, flash
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv
import sys


class Visitors:

    @staticmethod
    def profile_view(studentId):
        student = User.query.filter(User.id == studentId).one()
        return render_template('visitor/profileView.html', student=student)

    @staticmethod
    def homepage():
        return render_template('visitor/homepage.html',
                               positions=Position.query.filter(Position.available == True).order_by(
                                         Position.id.desc()).limit(5),
                               companies=Company.query.all())

    @staticmethod
    def apply_student(position_id):
        if session['type'] != 'Student':
            session['redirect'] = url_for('v1pre_routes.apply_students', position=position_id)
            return redirect(url_for('student_signup'))
        else:
            student = User.query.filter(User.id == session['id']).one()
            if student.cv_id is None:
                create_cv(User.query.filter(User.id == session['id']).one())
            try:
                if request.args['cv_confirmed'] != '1':
                    raise Exception('Not confirmed')
            except:
                session['redirect'] = request.full_path + 'cv_confirmed=1'
                return redirect(url_for('v1pre_routes.cv_confirm'))
            position_id = int(position_id)
            insert_application(session['id'], position_id, Position.query.filter(Position.id==position_id).one().company_id);
            flash('Кандидатстването Ви беше успешно.<style>.formater { background: transparent !important; }</style>', 'success')
            return render_template('visitor/profileView.html', student=student)

    @staticmethod
    def browse_offers():
        page = int(request.args.get('page', default='0'))
        offers_per_page = 10
        position = -2
        if request.form.get('position'):
            position = int(request.form.get('position'))

        company_id = -1
        if request.form.get('company'):
            company_id = int(request.form.get('company'))

        if position == -2:
            positions = Position.query.filter(Position.available == True)

        elif position == 1:
            positions = Position.query.filter(Position.available == True)\
                                   .filter(Position.tag_id <= 9)

        elif position == 10:
            positions = Position.query.filter(Position.available == True)\
                                   .filter(Position.tag_id > 9)\
                                   .filter(Position.tag_id <= 14)

        elif position == 15:
            positions = Position.query.filter(Position.available == True)\
                                   .filter(Position.tag_id > 14)\
                                   .filter(Position.tag_id <= 21)

        elif position == 22:
            positions = Position.query.filter(Position.available == True)\
                                   .filter(Position.tag_id > 21)\
                                   .filter(Position.tag_id <= 28)

        elif position == 29:
            positions = Position.query.filter(Position.available == True)\
                                   .filter(Position.tag_id > 28)\
                                   .filter(Position.tag_id <= 32)
        else:
            positions = Position.query.filter(Position.available == True)

        print(positions.all(), file=sys.stderr)
        if company_id != -1:
            print(company_id, file=sys.stderr)
            positions = positions.filter(Position.company_id == company_id)

        print(positions.all(), file=sys.stderr)
        positions = positions.order_by(Position.id.desc()).all()

        print(positions, file=sys.stderr)

        if len(positions) == 0:
            flash('За момента няма стажове за Вас.', 'warning')
            flash('Потърсете пак по-късно.', 'info')

        return render_template('visitor/browse.html',
                               positions=positions,
                               tags=Tag.query.all(),
                               companies=Company.query.all())
