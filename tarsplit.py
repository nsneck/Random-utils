#!/usr/bin/env python3

import sys, io, os.path
import tarfile

usagetext = 'This script takes two arguments. First the path to an archive file you want to split, ' \
'and then the number of files you want to have your archive be split by.'
if len(sys.argv) < 3:
    print(usagetext)
    exit()
tarpath = sys.argv[1]
splitnum = sys.argv[2]
try:
    tarfile.is_tarfile(tarpath)
except FileNotFoundError:
    print("Couldn't find an archive with the path '{}'.".format(tarpath))
    exit()
if not splitnum.isdigit() or not int(splitnum) > 0:
    print("The second argument must be the number of files you want to have your archive split by, it must be positive and greater than 0.")
    exit()
archivename = os.path.splitext(os.path.basename(tarpath))[0] # just pick up the archive filename without path / extension
tar = tarfile.open(tarpath, 'r' or 'r:*')
newtar = None
splitnumcounter = 1
splitarchivenum = 1
newtarname = archivename + '_0.tar'

while True: # infinite loop, we break out of it once we've processed all TarFile members
    member = tar.next()
    if member is None:
        break
    if not member.isfile():
        continue # currently we just don't care about non-file stuff
    if splitnumcounter > int(splitnum):
        newtar.close()
        newtar = None # reset the newtar var so we create a new one with a new name
        splitnumcounter = 0
        newtarname = archivename + '_' + str(splitarchivenum) + '.tar'
        splitarchivenum += 1
    if newtar is None:
        newtar = tarfile.open(newtarname, 'a' or 'a:')
    file = tar.extractfile(member)
    file = io.BytesIO(file.read()) # I couldn't find a better way to perform this in-memory, so this'll do.
    newtar.addfile(member, file)
    splitnumcounter += 1
if newtar is not None:
    newtar.close()