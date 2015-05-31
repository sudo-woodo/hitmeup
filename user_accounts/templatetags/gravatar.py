from django_jinja import library
import urllib
import hashlib


@library.global_function
def gravatar_url(email, size=80):
    default = 'retro'

    url = "http://www.gravatar.com/avatar/" + \
          hashlib.md5(email.lower()).hexdigest() + "?"
    url += urllib.urlencode({'d': default, 's': str(size)})

    return url
