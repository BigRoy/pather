import os
import sys
import logging

import nose

# Expose package
path = os.path.dirname(__file__)
sys.path.insert(0, path)


if __name__ == "__main__":
    argv = sys.argv[:]
    argv.extend(['--verbose', '--nocapture'])
    nose.main(argv=argv)
    os._exit(0)
