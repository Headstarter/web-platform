from functools import wraps
from flask import session, flash, render_template

class require(object):

	def __init__(self, role):
		self.role = role

	def __call__(self, f):

		@wraps(f)
		def wrapped_f(*args, **kwargs):
			if session.get('type') != self.role:
				flash('Permission denied. (requires role="' + (self.role or "None") + '", your is role="' + str (session.get ('type')) + '")', 'danger')
				flash('Please, log in as a ' + (self.role or "None") + ' to be able to visit this part of our platform.', 'info')
				return render_template ('template.html')
			else:
				return f(*args, **kwargs)
		return wrapped_f

