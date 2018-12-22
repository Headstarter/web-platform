from flask import Flask, render_template
app = Flask (__name__)

from flask_babel import Babel, gettext
app.config.from_pyfile ('config.cfg')
babel = Babel (app)

from flask import g, request

@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	print (translations)
	return request.accept_languages.best_match(translations)

@app.route ('/')
def index ():
   return render_template ('index.html')

@app.route ('/company/<companyId>', methods = ['GET', 'POST'])
def basic_company_profile_view (companyId):
	return ''

@app.route ('/companies', methods = ['GET', 'POST'])
def basic_company_profile_view (companyId):
	return ''

if __name__ == '__main__':
   app.run ()
