"""
WSGI config for gammelnok project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gammelnok.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from opbeat.contrib.django.middleware.wsgi import Opbeat

class MyCling(Cling):
    def _should_handle(self, path):
        """Checks if the path should be handled. Ignores the path if:

        * the host is provided as part of the base_url
        * the request's path isn't under the media path (or equal)
        """
        import glog
        print glob.glob('*')
        return path.startswith(self.base_url[2]) and not self.base_url[1]


application = get_wsgi_application()
application = MyCling(application)
application = Opbeat(application)
