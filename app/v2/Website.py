from app.v2.IWebsite import *
from app.v2.visitor import Visitor
from app.v2.students import Students
from app.v2.companies import Companies

class Website (IWebsite):

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
    
    def edit_position(self, positionId):
        return self.role_class[session['type']].edit_position(positionId)

    def list_my_positions(self):
        return self.role_class[session['type']].list_my_positions()

    def list_my_candidates(self):
        return self.role_class[session['type']].list_my_candidates()
    
    def faq(self):
        return self.role_class[session['type']].faq()
        
    def news(self):
        return self.role_class[session['type']].news()

    def media(self, id):
        return self.role_class[session['type']].media()

    def blog_posts(self):
        return self.role_class[session['type']].blog_posts()

    def about(self):
        return self.role_class[session['type']].about()


routes = Blueprint('core', __name__)
websiteSingleton = Website()

routes.add_url_rule('/'                           , endpoint='homepage'          , view_func=lambda: websiteSingleton.homepage(), methods=['GET'])
routes.add_url_rule('/faq'                        , endpoint='faq'               , view_func=lambda: websiteSingleton.faq(), methods=['GET'])
routes.add_url_rule('/news'                       , endpoint='news'              , view_func=lambda: websiteSingleton.news(), methods=['GET'])
routes.add_url_rule('/media/<id>'                 , endpoint='media'             , view_func=lambda: websiteSingleton.media(), methods=['GET'])
routes.add_url_rule('/about'                      , endpoint='about'             , view_func=lambda: websiteSingleton.about(), methods=['GET'])
routes.add_url_rule('/blog/posts/<id>'            , endpoint='blog_posts'        , view_func=lambda: websiteSingleton.blog_posts(), methods=['GET'])
routes.add_url_rule('/browse'                     , endpoint='browse_positions'  , view_func=lambda: websiteSingleton.browse_positions(), methods=['GET', 'POST'])
routes.add_url_rule('/positions/<positionId>'     , endpoint='position_details'  , view_func=lambda: websiteSingleton.position_details(), methods=['GET'])
routes.add_url_rule('/positions/my'               , endpoint='list_my_positions' , view_func=lambda: websiteSingleton.list_my_positions(), methods=['GET'])
routes.add_url_rule('/positions/new'              , endpoint='publish_position'  , view_func=lambda: websiteSingleton.publish_position(), methods=['GET', 'POST'])
routes.add_url_rule('/positions/<positionId>/edit', endpoint='edit_position'     , view_func=lambda: websiteSingleton.edit_position(), methods=['GET', 'POST'])
routes.add_url_rule('/applicants/my'              , endpoint='list_my_candidates', view_func=lambda: websiteSingleton.list_my_candidates(), methods=['GET'])
routes.add_url_rule('/profile/my'                 , endpoint='your_profile'      , view_func=lambda: websiteSingleton.your_profile(), methods=['GET'])
routes.add_url_rule('/profile/edit'               , endpoint='edit_profile'      , view_func=lambda: websiteSingleton.edit_profile(), methods=['GET', 'POST'])
routes.add_url_rule('/profile/picture/upload'     , endpoint='upload_picture'    , view_func=lambda: websiteSingleton.upload_picture(), methods=['POST'])
routes.add_url_rule('/profile/<id>/cv'            , endpoint='view_cv'           , view_func=lambda: websiteSingleton.view_cv(), methods=['GET'])
routes.add_url_rule('/company/<id>'               , endpoint='company_preview'   , view_func=lambda: websiteSingleton.company_preview(), methods=['GET'])
