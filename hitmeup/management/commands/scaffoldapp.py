from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import errno


class Command(BaseCommand):
    help = "Scaffolds an app directory with the typical directories and files you need."
    missing_args_message = "You must provide an app directory."

    TABS = "    "

    def add_arguments(self, parser):
        parser.add_argument('app', metavar='directory', help="the directory to scaffold")

    def handle(self, *args, **options):
        app = options['app']

        # check if folder exists
        if not os.path.isdir(app):
            raise CommandError("App directory \"%s\" does not exist." % app)

        # generate dirs
        for path, desc in getattr(settings, 'SCAFFOLDAPP_DIRS', []):
            path = path.format(app=app)
            desc = desc.format(app=app)

            self.stdout.write("Making directory {path}, which {desc}...".format(path=path, desc=desc))
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(path):
                    self.stdout.write(self.TABS + "%s already exists." % path)
                else: raise

        # generate files
        for path, desc in getattr(settings, 'SCAFFOLDAPP_FILES', []):
            path = path.format(app=app)
            desc = desc.format(app=app)

            self.stdout.write("Making file {path}, which {desc}...".format(path=path, desc=desc))
            # make containing dir
            container = os.path.dirname(path)
            try:
                os.makedirs(container)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(container): pass
                else: raise
            # make file
            try:
                open(path).close()
            except IOError:
                open(path, 'a+').close()
            else:
                self.stdout.write(self.TABS + "%s already exists." % path)

        self.stdout.write('Done.')
