from app.v2.WebsiteGenerator import *

routes = Blueprint('core', __name__)

class Website:
    _websiteSingleton = WebsiteGenerator()
    @classmethod
    def get_website(cls):
        return cls._websiteSingleton

routes.add_url_rule('/'                           , endpoint='homepage'          , view_func=lambda: Website.get_website().homepage()          , methods=['GET'        ])
routes.add_url_rule('/faq'                        , endpoint='faq'               , view_func=lambda: Website.get_website().faq()               , methods=['GET'        ])
routes.add_url_rule('/news'                       , endpoint='news'              , view_func=lambda: Website.get_website().news()              , methods=['GET'        ])
routes.add_url_rule('/media/<id>'                 , endpoint='media'             , view_func=lambda: Website.get_website().media()             , methods=['GET'        ])
routes.add_url_rule('/about'                      , endpoint='about'             , view_func=lambda: Website.get_website().about()             , methods=['GET'        ])
routes.add_url_rule('/blog/posts/<id>'            , endpoint='blog_posts'        , view_func=lambda: Website.get_website().blog_posts()        , methods=['GET'        ])
routes.add_url_rule('/browse'                     , endpoint='browse_positions'  , view_func=lambda: Website.get_website().browse_positions()  , methods=['GET', 'POST'])
routes.add_url_rule('/positions/<positionId>'     , endpoint='position_details'  , view_func=lambda: Website.get_website().position_details()  , methods=['GET'        ])
routes.add_url_rule('/positions/my'               , endpoint='list_my_positions' , view_func=lambda: Website.get_website().list_my_positions() , methods=['GET'        ])
routes.add_url_rule('/positions/new'              , endpoint='publish_position'  , view_func=lambda: Website.get_website().publish_position()  , methods=['GET', 'POST'])
routes.add_url_rule('/positions/<positionId>/edit', endpoint='edit_position'     , view_func=lambda: Website.get_website().edit_position()     , methods=['GET', 'POST'])
routes.add_url_rule('/applicants/my'              , endpoint='list_my_candidates', view_func=lambda: Website.get_website().list_my_candidates(), methods=['GET'        ])
routes.add_url_rule('/profile/my'                 , endpoint='your_profile'      , view_func=lambda: Website.get_website().your_profile()      , methods=['GET'        ])
routes.add_url_rule('/profile/edit'               , endpoint='edit_profile'      , view_func=lambda: Website.get_website().edit_profile()      , methods=['GET', 'POST'])
routes.add_url_rule('/profile/picture/upload'     , endpoint='upload_picture'    , view_func=lambda: Website.get_website().upload_picture()    , methods=[       'POST'])
routes.add_url_rule('/profile/<id>/cv'            , endpoint='view_cv'           , view_func=lambda: Website.get_website().view_cv()           , methods=['GET'        ])
routes.add_url_rule('/company/<id>'               , endpoint='company_preview'   , view_func=lambda: Website.get_website().company_preview()   , methods=['GET'        ])