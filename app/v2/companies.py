from app.v2.IWebsite import *
from app.v2.visitor import Visitor

class Companies (Visitor):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    @classmethod
    def _allowed_image(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
 
    def version(self):
        return "1.0"

    def template_folder(self): 
        return 'companies'
    
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
            if file and allowed_image(file.filename):
                import os
                saved = False
                where = 'static/headstarter/images/' + self.template_folder() + '/' + str(Company.query.filter(Company.id == session['company_id']).one().uid) + '.png'
                where_db = where[20:]
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
                        shutil.copy(os.path.join(os.environ['basedir'], 'static/headstarter/images/students/150.png'), 
                                      where)
                    except TypeError:
                        import sys
                        print('TypeError', file=sys.stderr)
                        company_uid = Company.query.filter(Company.id == session['company_id']).one().uid
                        print('company_uid', company_uid, file=sys.stderr)
                        Company.query.filter(Company.uid == company_uid).update({'logo': where_db});
                        db.session.commit()

                return jsonify({'value': 'Uploaded'}), 200
    
    def edit_profile(self):
        curr_company = Company.query.filter(Company.id == int(session['company_id'])).all()
        print(curr_company)
        if len(curr_company) != 1:
            flash('This offer not found.', 'info')
            return render_template("404.html"), 404
        
        curr_position = curr_company[0]
        
        import sys
        print('\n\n', curr_position, '\n\n')
        import sys
        print('\n\n' + str(dict(request.form)) + '\n\n')
        update_company(session['company_id'],
                        request.form['company-name'],
                        request.form['website'],
                        request.form['description'])

        return my_redirect(url_for('core.list_my_positions'))
    
    def homepage(self):
        return render_template('core/' + self.language + '/' + self.template_folder() + '/index.html',
                                tags=Tag.query.all(),
                                number_offers=Position.query.filter(Position.available == True).count(),
                                open=Target_Group.groupTags(session['company_id']),
                                positions=Position.query.filter(Position.available == True)
                                                        .order_by(Position.id.desc())
                                                        .limit(5))

    def publish_position(self):
        if request.method == 'GET':
            return render_template('core/' + self.language + '/' + self.template_folder() + '/post-offer.html', positionId=-1, tags=Tag.query.all())
        else:
            import sys
            print('\n\n' + str(dict(request.form)) + '\n\n')
            positionId = -1
            if request.form['id'] == '-1':
                positionId = insert_position(request.form['job-title'],
                                request.form['email'],
                                request.form['location'],
                                session['company_id'],
                                request.form['description'],
                                True if request.form['job-available'] == 'True' else False,
                                request.form['duration'],
                                request.form['job-type'],
                                request.form['job-age'],
                                request.form['job-category'])
            elif Position.query.filter(Position.id == int(request.form['id'])).count() == 1 and \
                    Position.query.filter(Position.id == int(request.form['id'])).one().company_id == session['company_id']:
                positionId = update_position(
                                request.form['id'],
                                request.form['email'],
                                request.form['location'],
                                request.form['job-title'],
                                session['company_id'],
                                request.form['description'],
                                True if request.form['job-available'] == 'True' else False,
                                request.form['duration'],
                                request.form['job-type'],
                                request.form['job-age'],
                                request.form['job-category'])
            else:
                return render_template('404.html'), 404

            print('BOOLEAN:', True if request.form['job-available'] == 'True' else False, file=sys.stderr)
            return my_redirect(url_for('core.list_my_positions'))

    def edit_position(self, positionId):
        curr_position = Position.query.filter(Position.id == int(positionId)).all()
        
        if len(curr_position) != 1:
            flash('This offer not found.', 'info')
            return render_template("404.html"), 404
        
        curr_position = curr_position[0]
        
        if curr_position.company_id != session['company_id']:
            flash('This offer is not yours.', 'info')
            return render_template("404.html"), 404
        
        import sys
        print('\n\n', curr_position, '\n\n')
        if request.method == 'GET':
            return render_template('core/' + self.language + '/' + self.template_folder() + '/post-offer.html', positionId=positionId, tags=Tag.query.all(), position=curr_position)
        else:
            import sys
            print('\n\n' + str(dict(request.form)) + '\n\n')
            positionId = update_position(
                            positionId,
                            request.form['email'],
                            request.form['location'],
                            request.form['job-title'],
                            session['company_id'],
                            request.form['description'],
                            True if request.form['job-available'] == 'True' else False,
                            request.form['duration'],
                            request.form['job-type'],
                            request.form['job-age'],
                            request.form['job-category'])
            print('BOOLEAN:', True if request.form['job-available'] == 'True' else False, file=sys.stderr)

            return my_redirect(url_for('core.list_my_positions'))
    
    def list_my_positions(self):
        positions = []
        import sys
        print(request.form.get('tag'))
        print(request.args.get('tag'))
        if request.args.get('tag') and request.args['tag'] != '0':
            positions = filter_all_offers_by_tag(int(request.args['tag']), session['company_id'])
        else:
            positions = filter_all_offers_by_tag(company=session['company_id'])
   
        if positions.count() == 0:
            flash('Нямате публикувани обяви все още.');
        
        return render_template('core/' + self.language + '/' + self.template_folder() + '/list_offers.html',
                               tags=Tag.query.all(),
                               positions=positions.all()
                               )
    
    def position_details(self, id):
        try:
            return render_template('core/' + self.language + '/' + self.template_folder() + '/offer-details.html',
                                   recents=Position.query.filter(Position.available == True)
                                   .order_by(Position.id.desc())
                                   .limit(5).all()
                                   ,
                                   offer=Position.query.filter(Position.available == True)
                                   .filter(Position.id == id).one())
        except:
            flash('This offer was not found.', "warn")
            return render_template("404.html"), 404
    
    def list_my_candidates(self):
        candidates = []
        import sys
        print(request.form.get('tag'))
        print(request.args.get('tag'))
        if request.args.get('tag') and request.args['tag'] != '0':
            candidates = filter_applications(int(request.args['tag']), session['company_id'])
        else:
            candidates = filter_applications(company=session['company_id'])
        
        # JUST TESTING = REMOVE BEFORE RELEASE
        if candidates.count() == 0:
            flash('Все още няма постъпили кандидати', 'info')
            
        return render_template('core/' + self.language + '/' + self.template_folder() + '/list_candidates.html',
                               tags=Position.query.filter(Position.company_id == session['company_id']).all(),
                               candidates=candidates.all()
                               )
    
    def your_profile(self):
        company = Company.query.filter(Company.id == session['company_id']).one()
        return render_template('core/' + self.language + '/' + self.template_folder() + '/profile.html', company=company)

