#!/usr/bin/python
import os
import sys
import re
import argparse

relativeHome='./'
pythonVersion='python2.7'
dataDir=relativeHome+'data/'
srcDir=relativeHome+'labelSrc/'
outDir=relativeHome+'output/'
sys.path.insert(0,dataDir)
sys.path.insert(0,srcDir)
from labelSrc import *


abbreviations={\
'measure'   :'Measure label',\
'mbe'       :'Measure minimum bounding ellipsoid',\
'extract'   :'Extract label',\
'remove'    :'Remove label'}

helpTable='\nabbreviation Table:\n\n'
for key in abbreviations:
    helpTable+=(key+'\t:'+abbreviations[key]+'\n')


procedures={\
'measure'   :['stats.py 9mo.label.gwm.nii.gz -v'],\
'mbe'       :['ellipsoid.py 9mo.label.gwm.nii.gz -v'],\
'extract'   :['extract.py 9mo.label.gwm.nii.gz -x 1 2 3 --out 123.nii.gz',\
              'stats.py 123.nii.gz -v'],
'remove'    :['remove.py 123.nii.gz -r 2 --out 13.nii.gz',\
              'stats.py 13.nii.gz -v']\
}

if not os.path.exists(outDir):
    os.makedirs(outDir)

if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser(description='Process labels.\n', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-o', metavar='abbr',type=str,nargs='+',
        help='define the order of calculations\n'+helpTable)
        args = parser.parse_args()

        if args.o==None:
            order=procedures
        else:
            order=args.o

        for p in order:
            print ('******************* '+abbreviations[p]+' *******************')
            print
            commands=procedures[p]
            for c in commands:
                print ('# '+c+' #')
                fileName,argument=c.split(' ',1)
                saveTo= ' > '+outDir+argument.split(' ',1)[0]+'.dat'
                os.system(pythonVersion+' '+srcDir+fileName+' '+dataDir+argument+saveTo)
                os.system('cat'+' '+outDir+argument.split(' ',1)[0]+'.dat')
                os.system('mv'+' '+argument.split(' ',1)[0]+' '+outDir)
                print('---------------------')
                # add validation codes here process here.

            print
    except KeyboardInterrupt:
        pass
