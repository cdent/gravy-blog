"""
Common test tasks.
"""

from google.appengine.ext import testbed


def data_setup():
    databed = testbed.Testbed()
    databed.activate()
    databed.init_datastore_v3_stub()
    databed.init_memcache_stub()
    databed.init_user_stub()
    return databed


def data_teardown(databed):
    databed.deactivate()
