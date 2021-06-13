from app.v2.IWebsite import *
from app.v2.visitor import Visitor
from app.v2.students import Students
from app.v2.companies import Companies

class WebsiteGenerator(IWebsite):

    def __init__(self):
        super().__init__()
        self.role_class = {
            'Visitor': Visitor(),
            'Student': Students(),
            'Company': Companies()
        }
    
    def version(self):
        return '1.0'

    def homepage(self): 
        return self.role_class[session['type']].homepage()

    def position_details(self, id): 
        return self.role_class[session['type']].position_details()

    def browse_positions(self): 
        return self.role_class[session['type']].browse_positions()

    def your_profile(self): 
        return self.role_class[session['type']].your_profile()

    def view_cv(self, id): 
        return self.role_class[session['type']].view_cv()

    def company_preview(self, id): 
        return self.role_class[session['type']].company_preview()

    def edit_profile(self):
        return self.role_class[session['type']].edit_profile()

    def upload_picture(self):
        return self.role_class[session['type']].upload_picture()

    def cv_confirm(self):
        return self.role_class[session['type']].cv_confirm()
    
    def publish_position(self):
        return self.role_class[session['type']].publish_position()
    
    def edit_position(self, id):
        return self.role_class[session['type']].edit_position(id)

    def list_my_positions(self):
        return self.role_class[session['type']].list_my_positions()

    def list_my_candidates(self):
        return self.role_class[session['type']].list_my_candidates()
    
    def faq(self):
        return self.role_class[session['type']].faq()
        
    def news(self):
        return self.role_class[session['type']].news()

    def media(self, id):
        return self.role_class[session['type']].media(id)

    def blog_posts(self, id):
        return self.role_class[session['type']].blog_posts(id)

    def about(self):
        return self.role_class[session['type']].about()
