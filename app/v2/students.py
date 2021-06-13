from app.v2.IWebsite import *
from app.v2.visitor import Visitor

class Students (Visitor):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    @classmethod
    def _allowed_image(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
 
    def version(self):
        return "1.0"

    def template_folder(self): 
        return 'students'

    def homepage(self): 
        return render_template('core/' + self.language + '/' + self.template_folder() + '/index.html',
                                tags=Tag.query.all(),
                                number_offers=Position.query.filter(
                                    Position.available == True
                                ).count(),
                                open=Target_Group.groupTags(),
                                positions=Position.query.filter(
                                    Position.available == True
                                )
                                .order_by(Position.id.desc())
                                .limit(5)
                            ) 

    def upload_picture(self):
        from flask import jsonify
        if request.method == 'POST':
            # check if the post request has the file part
            if 'logo' not in request.files:
                return jsonify({'value': 'No logo field available.'}), 400
            file = request.files['logo']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return jsonify({'value': 'No file selected.'}), 400
            if file and _allowed_image(file.filename):
                import os
                saved = False
                where = 'static/headstarter/images/' + self.template_folder() + '/' + str(User.query.filter(User.id == session['id']).one().id) + '.png'
                where_db = '/images/' + self.template_folder() + '/' + str(User.query.filter(User.id == session['id']).one().id) + '.png'
                where = os.path.join(os.environ['basedir'], where)
                os.system('echo > ' + where)
                with open(where, 'a'):
                    os.utime(where, None)
                while not saved:
                    import sys
                    try:
                        file.save(where)
                        saved = True
                        print('Saved', file=sys.stderr)
                    except FileNotFoundError:
                        print('FileNotFound', file=sys.stderr)
                        import shutil
                        shutil.copy(os.path.join(os.environ['basedir'], 'static/headstarter/images/' + self.template_folder() + '/150.png'), 
                                    where)
                    except TypeError:
                        import sys
                        print('TypeError', file=sys.stderr)
                        cv_id = User.query.filter(User.id == session['id']).one().cv_id
                        print('cv_id', cv_id, file=sys.stderr)
                        CV.query.filter(CV.id == cv_id).update({'photo': where_db});
                        db.session.commit()

                return jsonify({'value': 'Uploaded'}), 200

    def edit_profile(self):
        curr_user = User.query.filter(User.id == int(session['id'])).all()
        print(curr_user)
        if len(curr_user) != 1:
            flash('This offer not found.', 'info')
            return render_template("404.html"), 404
        
        curr_user = curr_user[0]
        
        import sys
        print('\n\n', curr_user, '\n\n')
        import sys
        print('\n\n' + str(dict(request.form)) + '\n\n')
        import json
        print('\n\n' + str(request.__dict__) + '\n\n')
        
        x = update_cv(session['id'],
                request.form['name'],
                request.form['email'],
                request.form['telephone'],
                request.form['location'],
                request.form['birthday'],
                request.form['languages'],
                request.form['education'],
                request.form['projects'],
                request.form['resume-content'],
                request.form['skills'],
                request.form['hobbies'])
        print('\n\n' + str(x) + '\n\n')
        
        return my_redirect(url_for('core.profile'))

    def your_profile(self):
        import sys
        student = User.query.filter(User.id == session['id']).one()
        try:
            print(student.cv.get_education())
        except:
            create_cv(student)
        student = User.query.filter(User.id == session['id']).one()
        return render_template('core/' + self.language + '/' + self.template_folder() + '/edit_cv.html', student=student)

    def cv_confirm(self):
        try:
            # return str(session['redirect'])
            if request.args['cv_confirmed'] == '1':
                return redirect(session['redirect'])
        except:
            pass
        student = User.query.filter(User.id == session['id'])[0]
        return render_template('visitor/profileView.html', student=student, current=request.full_path, confirm=url_for('v1pre_routes.profile',
                                                                                            studentId=session['id']))
