#!/usr/bin/env python
"""
Quick script to link a dependency into the repo without
having to copy it in or store it in the repo.
"""

import sys
import os

def run():
    for module in sys.argv[1:]:
        imported = __import__(module)
        path = os.path.dirname(imported.__file__)
        basename = os.path.basename(path)
        if not os.path.exists(basename):
            os.symlink(path, basename)

if __name__ == '__main__':
    run()
