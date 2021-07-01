#!/usr/bin/env python3
__author__ = "Grant Murphy, gcmurphy@protonmail.com"

import argparse
import logging
import os
import subprocess
import sys
from pycclib import compiler, linker
from pycclib.log import log


def main():

    flags = argparse.ArgumentParser(description='Python C compiler')
    flags.add_argument('sources', metavar='SOURCE', nargs='+')
    flags.add_argument('--output', default='a.out', help='compiled binary output file')
    opts = flags.parse_args()

    compiled = []
    for filename in opts.sources:
        with open(filename) as source:
            try:
                outfile = compiler.assembly_file(filename)
                with open(outfile, 'w') as dest:
                    compiler.compile(filename, source, dest)

                log.debug("generated: %s:\n%s", outfile, open(outfile).read())
                compiled.append(outfile)
            except Exception as err:
                log.error('an error occurred whilst compiling %s', filename)
                log.exception(err)
                sys.exit(1)


    if not linker.link(opts.output, compiled):
        log.error('failed to link file/s: ' + str(compiled))
        sys.exit(1)


if __name__ == "__main__":
    main()
