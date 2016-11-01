#!/usr/bin/env python

"""

"""
import os
import sys      
import numpy as np
import nibabel as nb
import pandas as pd
import scipy.ndimage as ndimage
import argparse

import iw_labels as labels
import iwUtilities as util

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='iw_compare_images')

     parser.add_argument("in_nii",    help="Filename of NIFTI input label ")
     inArgs = parser.parse_args()


     #
     
     in_label_nii    = labels.read_nifti_file( inArgs.in_nii, 'Label file does not exist' )
     
     labels = labels.get_labels( None, in_label_nii.get_data() )

     for ii in labels:
          print (ii)
