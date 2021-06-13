from app.v2.IWebsite import *

class Visitor (IWebsite):
    def version(self):
        return "1.0"

    def template_folder(self): 
        return 'visitor'

    def homepage(self): 
        print()
        print()
        print()
        print(Tag.query.all())
        print()
        print()
        print()
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

    def position_details(self, id): 
        try:
            return render_template('core/' + self.language + '/' + Visitors.folder() + '/offer-details.html',
                                   recents=Position.query.filter(
                                       Position.available == True)
                                   .order_by(Position.id.desc())
                                   .limit(5).all(),
                                   offer=Position.query.filter(
                                       Position.available == True)
                                   .filter(Position.id == id).one())
        except:
            flash('This offer was not found.', "warn")
            return render_template("404.html"), 404

    def browse_positions(self): 
        positions = []
        print(request.args.get('tag'))
        print(request.args.get('company'))
        company = request.args.get('company') or '0'
        tag = request.args.get('tag') or '0'
        group = request.args.get('group') or '-1'
        if group == '-1':
            if company == '0' and tag == '0':
                positions = filter_offers_by_tag()
            elif company == '0' and tag != '0':
                positions = filter_offers_by_tag(int(tag))
            elif tag == '0' and company != '0':
                positions = filter_offers_by_tag(company=int(company))
        else:
            positions = filter_offers_by_tag(group=int(group))

        return render_template('core/' + self.language + '/' + self.template_folder() + '/browse.html',
                               tags=Tag.query.all(),
                               companies=Company.query.all(),
                               positions=positions,
                               company_selected=int(company),
                               tag_selected=int(tag),
                               )

    def your_profile(self):
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Student"))

    def view_cv(self, id):
        student = User.query.filter(User.id == id)[0]
        return render_template('core/' + self.language + '/' + self.template_folder() + '/profileView.html', student=student)

    def company_preview(self, id): 
        company = Company.query.filter(Company.id == id)[0]
        return render_template('core/' + self.language + '/' + self.template_folder() + '/company-page.html', company=company, 
                               open=Position.query.filter(Position.company_id == id).filter(Position.available == True).count(),
                               positions=Position.query.filter(Position.company_id == id).filter(Position.available == True).all())

    def news(self):
        return render_template('core/' + self.language + '/' + self.template_folder() + '/news.html')

    def faq(self):
        return render_template('core/' + self.language + '/' + self.template_folder() + '/faq.html')
    
    def media(self, id):
        if str(id) == "0":
            return redirect("http://news.bnt.bg/bg/a/mladezhi-spechelikha-sstezanie-s-platforma-za-namirane-na-stazh#")
        elif str(id) == "1":
            return redirect("https://www.bloombergtv.bg/update/2019-06-02/kakvi-vazmozhnosti-pred-uchenitsite-i-biznesa-dava-programata-teenovator")
        elif str(id) == "2":
            return redirect("http://bnr.bg/horizont/post/101157715/onlain-platforma-tarsi-stajove-za-uchenici")

    def blog_posts(self):
        if str(id) == "1":
            return render_template('core/' + self.language + '/' + self.template_folder() + '/how_to_cv.html')
        elif str(id) == "2":
            return render_template('core/' + self.language + '/' + self.template_folder() + '/how_to_hire.html')
        elif str(id) == "3":
            return render_template('core/' + self.language + '/' + self.template_folder() + '/how_to_choose_job.html')
    
    def about(self):
        return render_template('core/' + self.language + '/' + self.template_folder() + '/about.html', students = 567, companies = Company.query.count(), offers = Position.query.count())
