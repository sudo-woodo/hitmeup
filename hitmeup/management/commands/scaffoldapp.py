from django.core.management.base import BaseCommand, CommandError
import os
import errno

class Command(BaseCommand):
    help = "Scaffolds an app directory with the typical directories and files you need."
    missing_args_message = "You must provide an app directory."

    TABS = "    "

    DIRS = [
        (os.path.join('{app}', 'static'), "holds project static assets"),
        (os.path.join('{app}', 'static', '{app}'), "holds {app}'s static assets"),
        (os.path.join('{app}', 'static', '{app}', 'js'), "holds {app}'s Javascript files"),
        (os.path.join('{app}', 'static', '{app}', 'css'), "holds {app}'s CSS files"),
        (os.path.join('{app}', 'static', '{app}', 'img'), "holds {app}'s image files"),
        (os.path.join('{app}', 'templates'), "holds project templates"),
        (os.path.join('{app}', 'templates', '{app}'), "holds {app}'s templates"),
    ]

    FILES = [
        (os.path.join('{app}', 'urls.py'), "describes {app}'s routes")
    ]

    def add_arguments(self, parser):
        parser.add_argument('app', metavar='directory', help="the directory to scaffold")

    def handle(self, *args, **options):
        app = options['app']

        if not os.path.isdir(app):
            raise CommandError("App directory \"%s\" does not exist." % app)

        for path, desc in self.DIRS:
            path = path.format(app=app)
            desc = desc.format(app=app)

            self.stdout.write("Making directory {path}, which {desc}...".format(path=path, desc=desc))
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(path):
                    self.stdout.write(self.TABS + "%s already exists." % path)
                else:
                    raise

        for path, desc in self.FILES:
            path = path.format(app=app)
            desc = desc.format(app=app)

            self.stdout.write("Making file {path}, which {desc}...".format(path=path, desc=desc))
            try:
                open(path).close()
            except IOError:
                open(path, 'a+').close()
            else:
                self.stdout.write(self.TABS + "%s already exists." % path)

        self.stdout.write('Done.')
