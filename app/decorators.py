from functools import wraps
from flask import session, flash, render_template

class require(object):

	def __init__(self, role):
		self.role = role

	def __call__(self, f):

		@wraps(f)
		def wrapped_f(*args, **kwargs):
			if session.get('type') != self.role:
				flash('Permission denied. (requires role="' + self.role + '", your is role="' + str (session.get ('type')) + '")', 'danger')
				return render_template ('template.html')
			else:
				return f(*args, **kwargs)
		return wrapped_f

