import shutil
import tempfile
from django.test.utils import override_settings
import os
from StringIO import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from hitmeup import settings


TEST_SCAFFOLDAPP_DIRS = [
    (os.path.join('{app}', 'static'), "holds project static assets"),
    (os.path.join('{app}', 'static', '{app}'), "holds {app}'s static assets"),
    (os.path.join('{app}', 'static', '{app}', 'js'), "holds {app}'s Javascript files"),
    (os.path.join('{app}', 'static', '{app}', 'css'), "holds {app}'s CSS files"),
    (os.path.join('{app}', 'static', '{app}', 'img'), "holds {app}'s image files"),
    (os.path.join('{app}', 'templates'), "holds project templates"),
    (os.path.join('{app}', 'templates', '{app}'), "holds {app}'s templates"),
    (os.path.join('{app}', 'something', '{app}', 'somethingelse'), "test -p functionality"),
    ]

TEST_SCAFFOLDAPP_FILES = [
    (os.path.join('{app}', 'urls.py'), "describes {app}'s routes"),
    (os.path.join('{app}', 'unmade', 'folder', 'urls.py'), "test -p functionality"),
]


@override_settings(SCAFFOLDAPP_DIRS=TEST_SCAFFOLDAPP_DIRS, SCAFFOLDAPP_FILES=TEST_SCAFFOLDAPP_FILES)
class ScaffoldAppTestCase(TestCase):
    """
    Tests usage of `manage.py scaffoldapp`.
    """

    def setUp(self):
        # change to temp dir
        self.__orig_dir = os.path.dirname(os.path.abspath(__file__))
        self.__temp_dir = tempfile.mkdtemp()
        os.chdir(self.__temp_dir)

        # setup app dir
        self.app = 'app'
        os.mkdir(self.app)

    def tearDown(self):
        # restore
        os.chdir(self.__orig_dir)
        shutil.rmtree(self.__temp_dir)
        del self.__orig_dir
        del self.__temp_dir

    def test_normal(self):
        """
        Test the normal use case.
        """
        # set up mock stdout
        out = StringIO()
        call_command('scaffoldapp', self.app, stdout=out)

        # test dir generation
        for path, desc in settings.SCAFFOLDAPP_DIRS:
            path = path.format(app=self.app)
            desc = desc.format(app=self.app)

            self.assertTrue(os.path.isdir(os.path.join(self.__temp_dir, path)),
                            "Directory \"%s\" does not exist" % path)
            self.assertIn(desc, out.getvalue(), "Description \"%s\" not in stdout" % desc)

        # test file generation
        for path, desc in settings.SCAFFOLDAPP_FILES:
            path = path.format(app=self.app)
            desc = desc.format(app=self.app)

            self.assertTrue(os.path.isfile(os.path.join(self.__temp_dir, path)),
                            "File \"%s\" does not exist" % path)
            self.assertIn(desc, out.getvalue(), "Description \"%s\" not in stdout" % desc)

    def test_requires_arg(self):
        """
        Test that scaffoldapp fails with inappropriate args.
        """
        # test no args
        with self.assertRaises(CommandError):
            call_command('scaffoldapp')

        # test too many args
        with self.assertRaises(CommandError):
            call_command('scaffoldapp', 'extraneous', 'args')

    def test_requires_directory(self):
        """
        Test that scaffoldapp fails when a directory that doesn't exist is provided.
        """
        with self.assertRaises(CommandError):
            call_command('scaffoldapp', 'DOES_NOT_EXIST')

    def test_partial_directories(self):
        """
        Test that the correct messages print for already existing directories
        """
        # set up mock stdout
        out = StringIO()

        # make half the dirs
        made_dirs = settings.SCAFFOLDAPP_DIRS[:len(settings.SCAFFOLDAPP_DIRS)//2]
        for path, desc in made_dirs:
            path = path.format(app=self.app)
            os.makedirs(path)

        # make half the files
        made_files = settings.SCAFFOLDAPP_FILES[:len(settings.SCAFFOLDAPP_FILES)//2]
        for path, desc in made_files:
            path = path.format(app=self.app)
            open(path, 'a+').close()

        call_command('scaffoldapp', self.app, stdout=out)

        # assert the correct message shows up in dir generation
        msg = "already exists"
        for item in settings.SCAFFOLDAPP_DIRS:
            path, desc = item
            path = path.format(app=self.app)
            desc = desc.format(app=self.app)

            self.assertTrue(os.path.isdir(os.path.join(self.__temp_dir, path)),
                            "Directory \"%s\" does not exist" % path)

            if item in made_dirs:
                self.assertIn(desc, out.getvalue(), "Message \"%s\" is not in stdout" % msg)
            else:
                self.assertIn(desc, out.getvalue(), "Description \"%s\" not in stdout" % desc)

        # assert the correct message shows up in file generation
        for item in settings.SCAFFOLDAPP_FILES:
            path, desc = item
            path = path.format(app=self.app)
            desc = desc.format(app=self.app)

            self.assertTrue(os.path.isfile(os.path.join(self.__temp_dir, path)),
                            "File \"%s\" does not exist" % path)

            if item in made_files:
                self.assertIn(desc, out.getvalue(), "Message \"%s\" is not in stdout" % msg)
            else:
                self.assertIn(desc, out.getvalue(), "Description \"%s\" not in stdout" % desc)

