__author__ = "Grant Murphy, gcmurphy@protonmail.com"

import subprocess
import os
from pycclib.log import log

def link(out, sources, *flags):
    cmd = [os.environ.get('CC', 'gcc'), '-o', out]
    cmd += flags
    cmd += sources
    log.debug('linking: %s', ' '.join(cmd))
    return 0 == subprocess.call(cmd)
