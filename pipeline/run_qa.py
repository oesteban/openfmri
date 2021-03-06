#!/usr/bin/env python
""" run_qa.py - run qa on all data

USAGE: python run_qa.py <name of dataset> <basedir - default is staged>
"""

## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import os,glob
import sys
import launch_qsub
from openfmri_utils import load_scankey

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    if len(sys.argv)>1:
        ds=sys.argv[1]
    else:
        usage()

    if len(sys.argv)>2:
        basedir=sys.argv[2]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        basedir='/corral-repl/utexas/poldracklab/openfmri/staged'
        

    sk=load_scankey(os.path.join(basedir,ds,'scan_key.txt'))
    TR=sk['TR']
    
    outfile=open('run_qa_%s.sh'%ds,'w')
    dsdir=os.path.join(basedir,ds)
    for d in glob.glob(os.path.join(dsdir,'sub*/BOLD/*/bold_mcf.nii.gz')):
                      outfile.write('fmriqa.py %s %s\n'%(d,sk['TR']))

    outfile.close()
    if float(sk['TR'])<2:
	queue='largemem'
	ncores=24
	print 'using largemem queue'
    else:
	queue='normal'
	ncores=12
    print 'now launching using:'
    print 'launch -s run_qa_%s.sh -n qa -r 00:30:00'%ds
    launch_qsub.launch_qsub(script_name='run_qa_%s.sh'%ds,runtime='00:30:00',jobname='%sqa'%ds,email=False,queue=queue,ncores=ncores)


if __name__ == '__main__':
    main()
