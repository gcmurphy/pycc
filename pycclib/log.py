__author__ = "Grant Murphy, gcmurphy@protonmail.com"
import os
import logging
if 'DEBUG' in os.environ:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
log = logging.getLogger('pycc')


