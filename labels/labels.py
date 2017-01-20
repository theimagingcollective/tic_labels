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

import _utilities as util


def read_nifti_file( nii_filename, error_message ):

    if os.path.isfile(nii_filename):
        try:
            nii = nb.load( nii_filename )
        except IOError:
            sys.exit("Unable to read NIFTI file")
    else:
        sys.exit(error_message)

    return nii

def read_labels_from_csv( filename ):

    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        csv_labels  = list(pd.to_numeric( df['label'].get_values()) )
    else:
        sys.exit('CSV file does not exist')

    return csv_labels


def read_from_csv( filename ):

    if os.path.isfile(filename):
        df = pd.read_csv(filename, header=None )
        
        # I need to figure out how to drop non numeric values without assumming that they are in the 
        # first row

        s  = [ pd.to_numeric( df.iloc[x,:], errors='coerce') for x in range(1, len(df.index)) ]
 #       s  = s.dropna()
        #csv_data = np.ndarray.tolist( s.values)        
    else:
        sys.exit('CSV file does not exist')

    return s # csv_data



def get_labels( requested_labels, label_array, include_background=False ):

    all_labels = np.unique(label_array[ label_array > 0 ])

    if requested_labels == None:  # In this case None means All labels present
        labels = all_labels
    else:
        labels = list( set(requested_labels) & set(all_labels))
    
    if include_background:
       labels = [ 0 ]  + labels


    if not len(labels) :
        sys.exit('Labels requested do not exist in the label array')

    return sorted( list(labels)) 


def image_shape_check( image_array ):

    if len(image_array.shape) < 2 or len(image_array.shape) > 4:
        sys.exit('Only supports 3D and 4D image arrays')


def individual_image_stats( image_array ) :

    label_mean   = np.mean( image_array )
    label_std    = np.std( image_array )
    label_min    = np.min( image_array )
    label_max    = np.max( image_array )

    return [label_mean, label_std, label_min, label_max]

def permute_image_array( image_array ):

    if len(image_array.shape) == 4:
        nVolumes = int(image_array.shape[3])
        image_array = np.transpose( image_array, [3,0,1,2] )
    else:
        nVolumes = 1
        image_array = np.expand_dims(image_array, axis=0)

    return image_array, nVolumes
