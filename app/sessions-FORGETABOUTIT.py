import os

from uuid import uuid1
from pickle import UnpicklingError, dumps, load
from contextlib import suppress
from flask.sessions import SessionInterface, SessionMixin


class PickleSession(SessionMixin):
    """Server-side session implementation.

    Uses pickle to achieve a disk-backed session such that multiple
    worker processes can access the same session data.
    """

    def __init__(self, directory, sid, *args, **kwargs):
        self.path = os.path.join(directory, sid)
        self.directory = directory
        self.sid = sid
        self.read()

    def __getitem__(self, key):
        self.read()
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    def __delitem__(self, key):
        del self.data[key]
        self.save()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def read(self):
        """Load pickle from (ram)disk."""
        try:
			with open(self.path, 'rb') as blob:
				# import sys
				# print('\t\t\t\t', blob.read(), file=sys.stderr)
				self.data = load(blob)
        except FileNotFoundError:
            import sys
            print("ДА МУ ЕБА МАЙКАТА НЕЩГО СТАНА FileNotFoundError", file=sys.stderr)
            self.data = {}
        except ValueError:
            import sys
            print("ДА МУ ЕБА МАЙКАТА НЕЩГО СТАНА ValueError", file=sys.stderr)
            self.data = {}
        except EOFError:
            import sys
            print("ДА МУ ЕБА МАЙКАТА НЕЩГО СТАНА EOFError", file=sys.stderr)
            self.data = {}
        except UnpicklingError:
            import sys
            print("ДА МУ ЕБА МАЙКАТА НЕЩГО СТАНА UnpicklingError", file=sys.stderr)
            self.data = {}
        except:
            self.data = {}
            import sys
            print("Can't load session information.", file=sys.stderr)

    def save(self):
        """Dump pickle to (ram)disk atomically."""
        with open(self.path, 'wb') as blob:
            blob.write(dumps(self.data))
            blob.close()

    # Note: Newer versions of Flask no longer require
    # CallableAttributeProxy and PersistedObjectProxy


class PickleSessionInterface(SessionInterface):
    """Basic SessionInterface which uses the PickleSession."""

    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)

    def open_session(self, app, request):
        sid = request.cookies.get(
            app.session_cookie_name) or '{}-{}'.format(uuid1(), os.getpid())
        return PickleSession(self.directory, sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            with suppress(FileNotFoundError):
                os.unlink(session.path)
            response.delete_cookie(
                app.session_cookie_name, domain=domain)
            return
        cookie_exp = ' 2999-12-31 23:59:59.999999'#self.get_expiration_time(app, session)
        import sys
        print("cookie_exp: ", cookie_exp, file=sys.stderr)
        response.set_cookie(
            app.session_cookie_name, session.sid,
            expires=cookie_exp, httponly=True, domain=domain)
