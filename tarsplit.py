#!/usr/bin/env python3

import sys
import io
import os.path
import tarfile
import argparse


class ArgumentParser(argparse.ArgumentParser):
    # We define a custom parser class in order to be able to override
    # the default error behavior. We want to print the help text
    # whenever the user makes a mistake so they can get a more
    # informative help message.
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


argparser = ArgumentParser(
    description='Split a tar archive into smaller '
    'archives by number of files inside each split archive.')
argparser.add_argument(
    'splitnum',
    metavar='N',
    type=int,
    help='The number of files you want to have each split '
    'archive be populated by.')
argparser.add_argument(
    'tarpath',
    metavar='I',
    type=str,
    help='The input tar archive that will be split to smaller archives.')
argparser.add_argument(
    '-o, --outputdir',
    dest='outputdir',
    default=os.path.dirname(os.path.abspath(__file__)),
    type=str,
    help='The output directory where split archives will be written to. '
    'Default is script execution directory.')
args = argparser.parse_args()
splitnum = args.splitnum
tarpath = args.tarpath
outputdir = args.outputdir
if not splitnum > 0:
    print("error: The first argument must be the number of files "
          "you want to have your archive split by, it must be positive "
          "and greater than 0.\n")
    argparser.print_help()
    exit()
try:
    tarfile.is_tarfile(tarpath)
except FileNotFoundError:
    print("Couldn't find an archive with the path '{}'.".format(tarpath))
    exit()
# Without a trailing '/' file handling inside the directory won't work
if not outputdir.endswith('/'):
    outputdir += '/'
if not os.path.isdir(outputdir):
    print("error: '{}' is not a directory.\n".format(outputdir))
    argparser.print_help()
    exit()

# just pick up the archive filename without path / extension
archivename = os.path.splitext(os.path.basename(tarpath))[0]
tar = tarfile.open(tarpath, 'r' or 'r:*')
newtar = None
splitnumcounter = 1
splitarchivenum = 1
newtarname = outputdir + archivename + '_0.tar'

# infinite loop, we break out of it once we've processed all TarFile members
while True:
    member = tar.next()
    if member is None:
        break
    if not member.isfile():
        continue  # currently we just don't care about non-file stuff
    if splitnumcounter > int(splitnum):
        newtar.close()
        # reset the newtar var so we create a new one with a new name
        newtar = None
        splitnumcounter = 1
        newtarname = outputdir + archivename + '_' + \
            str(splitarchivenum) + '.tar'
        splitarchivenum += 1
    if newtar is None:
        newtar = tarfile.open(newtarname, 'a' or 'a:')
    extractedfile = tar.extractfile(member)
    # I couldn't find a better way to perform this in-memory, so this'll do.
    extractedfile = io.BytesIO(extractedfile.read())
    newtar.addfile(member, extractedfile)
    splitnumcounter += 1
if newtar is not None:
    newtar.close()
