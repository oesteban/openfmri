#!/usr/bin/env python
""" mk_level3_fsf.py - make 3rd level (betwee-subjects) model
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




# create fsf file for arbitrary design
import numpy as N
import sys
import os
import subprocess as sub
from openfmri_utils import *

# create as a function that will be called by mk_all_fsf.py
# just set these for testing
taskid='ds002'
nsubs=17
tasknum=1
## nruns=6
#runs=[1,2]
copenum=1

basedir='/corral/utexas/poldracklab/openfmri/shared/'

def mk_level3_fsf(taskid,tasknum,nsubs,basedir):
#if 1==1:

    groupdir='%s/%s/group'%(basedir,taskid)
    if not os.path.exists(groupdir):
        os.mkdir(groupdir)
    modeldir='%s/%s/group/task%03d'%(basedir,taskid,tasknum)
    if not os.path.exists(modeldir):
        os.mkdir(modeldir)

    # read the conditions_key file
    cond_key=load_condkey(basedir+taskid+'/condition_key.txt')

    # figure out the number of copes
    conditions=cond_key[tasknum].values()
    ncopes=len(conditions)+1
    
    stubfilename='/corral/utexas/poldracklab/code/poldrack/openfmri/design_level3.stub'

    for copenum in range(1,ncopes+1):
        outfilename='%s/cope%03d.fsf'%(modeldir,copenum)
        print('%s\n'%outfilename)
        outfile=open(outfilename,'w')
        outfile.write('# Automatically generated by mk_fsf.py\n')

        # first get common lines from stub file
        stubfile=open(stubfilename,'r')
        for l in stubfile:
            outfile.write(l)

        stubfile.close()

        # now add custom lines

        outfile.write('\n\n### AUTOMATICALLY GENERATED PART###\n\n')

        outfile.write('set fmri(outputdir) "%s/cope%03d.gfeat"\n'%(modeldir,copenum))

        ngoodsubs=0
        for r in range(nsubs):
            featfile='%s%s/sub%03d/model/task%03d.gfeat/cope%d.feat'%(basedir,taskid,r+1,tasknum,copenum)
            if os.path.exists(featfile):
                outfile.write('set feat_files(%d) "%s"\n'%(ngoodsubs+1,featfile))
                outfile.write('set fmri(evg%d.1) 1\n'%int(ngoodsubs+1))
                outfile.write('set fmri(groupmem.%d) 1\n'%int(ngoodsubs+1))
                ngoodsubs+=1
                
        outfile.write('set fmri(npts) %d\n'%ngoodsubs) # number of runs
        outfile.write('set fmri(multiple) %d\n'%ngoodsubs) # number of runs

        outfile.close()
