from flask import Flask, render_template
app = Flask (__name__)

@app.route('/')
def index():
   return render_template ('index.html')

@app.route('/company/<companyId>', methods = ['GET', 'POST'])
def basic_company_profile_view (companyId):
	return ''

if __name__ == '__main__':
   app.run ()
