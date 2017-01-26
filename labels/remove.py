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

import labels
import _utilities as util

def remove(in_label_array,remove_labels):# function that can be called directly. in_label_array and remove_labels are passed on in raw python array format.
    out_label_array = in_label_array[:] # deep copy
    for ii in remove_labels:
        mask = in_label_array == ii
        out_label_array[ mask ] = 0
    return out_label_array
#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='iw_labels_remove')

     parser.add_argument("in_nii",    help="Filename of NIFTI input label ")
     parser.add_argument("--out_nii",    help="Filename of NIFTI output label. (default = --in_nii ) ")

     parser.add_argument('-r', "--remove",  help="Labels to remove", type=float, nargs="*", default = [] )
     parser.add_argument("--csv",           help="CSV filename containing labels to remove", default = [] )

     parser.add_argument("-v","--verbose",  help="Verbose flag",      action="store_true", default=False )
     
     try:   # Rz mod. This exception is already captured by the parser, so it's not quite necessary
         inArgs = parser.parse_args()
     except SystemExit:
         print ("You need to specify the input file!")
         exit(0)                     # Rz mod.

     in_label_nii    = labels.read_nifti_file( inArgs.in_nii, 'Label file does not exist' )
     in_label_array  = in_label_nii.get_data()
     #print (in_label_array.shape)         # Rz mod.

     if inArgs.out_nii == None:
          out_filename = inArgs.in_nii
     else:
          out_filename = inArgs.out_nii

     if len(inArgs.csv):
         csv_remove_labels = labels.read_labels_from_csv( inArgs.csv ) # Rz mod. the read_labels_from_csv already has exception handling. iw_labels has different ways of handling exceptions. Can be unified.
     else:
         csv_remove_labels = []

     remove_labels  = labels.get_labels( inArgs.remove + csv_remove_labels, in_label_array )

     if inArgs.verbose:
          print (sorted(inArgs.remove + csv_remove_labels))

     out_label_array=remove(in_label_array,remove_labels) # Rz mod. the part that calls function

     nb.save( nb.Nifti1Image( out_label_array, in_label_nii.get_affine()), out_filename )
