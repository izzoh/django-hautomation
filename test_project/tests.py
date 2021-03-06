#This file mainly exists to allow python setup.py test to work.
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings
from django.test.utils import setup_test_environment


def runtests():
    setup_test_environment()
    test_runner = get_runner(settings)
    test = test_runner(verbosity=1, interactive=True)
    failures = test.run_tests([])
    sys.exit(failures)


if __name__ == '__main__':
    unittest.main()
