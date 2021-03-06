#!/usr/bin/env python -i

""" A shell to play around with the local data, assuming:
dev_appserver.py . --use_sqlite --datastore_path=tmp/data """

import os
import logging
from lib import DATASTORE_PATH, setup_environ

setup_environ()

# Setup shell stubs

from google.appengine.tools import old_dev_appserver
from google.appengine.tools import dev_appserver_main

app_id = os.environ['APPLICATION_ID']

kwargs = dev_appserver_main.DEFAULT_ARGS.copy()

kwargs.update({
    'use_sqlite': True,
    'datastore_path': DATASTORE_PATH
    # todo: blobstore, prospective search
})
old_dev_appserver.SetupStubs(app_id, **kwargs)
logging.info('DataStore Path: %s' % DATASTORE_PATH)
