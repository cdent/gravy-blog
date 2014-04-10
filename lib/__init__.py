"""
Fiddle with the environment to make things work.

This borrows from djappengine environ.py but leaves out a lot
to make behaviors clear and more direct.
"""

import sys
import os

ROOT_PATH = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
DATASTORE_PATH = os.path.join(ROOT_PATH, 'tmp', 'data')


# Hardcoded for now
SDK_PATH = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine'


def setup_environ():
    sys.path.insert(0, SDK_PATH)

    from dev_appserver import fix_sys_path
    fix_sys_path()

    sys.path.insert(0, os.path.join(SDK_PATH, 'lib', 'django-1.4'))

    from google.appengine.tools import old_dev_appserver as tools_dev_appserver
    appinfo, url_matcher, from_cache = tools_dev_appserver.LoadAppConfig(
            ROOT_PATH, {}, default_partition='dev')
    app_id = appinfo.application

    # Useful for later scripts
    os.environ['APPLICATION_ID'] = app_id
    os.environ['APPLICATION_VERSION'] = appinfo.version
    os.environ['AUTH_DOMAIN'] = 'fakedomain.com'

    import settings
    from django.core.management import setup_environ
    setup_environ(settings, original_settings_path='settings')
