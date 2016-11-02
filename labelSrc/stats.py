#!/usr/bin/env python

"""
stats.py

Purpose of this function is to measure attributes of a label and/or statistics of an image constrained by the label

Requirements

1) Required Inputs
    3D or 4D Label NIFTI Image

   Optional Inputs
       List of 3D or 4D Images.  If 4D Label Image is given then each 3D Volume will be treated separately
       CSV output file containing measured metrics.  Pandas python library will be used to read and write CSV files.
       Display only option.  This option is helpful if you just want to obtain some quick information about the labels.

    The label image and optional input image shall have the same dimensions along the first three dimensions.  The
    fourth dimension may be different.  A 4D label image will be treated as if a list of 3D label images were given.
    The labels in each of the 3D label volumes may contain the same label but shall be treated separately.  If a 4D image
    file is given then statistics will be reported from each of the individual 3D volumes.


2) Output image shall always contain the following information

    Label Number (Integer or Floating Point Number)
    Label Center of Mass
    Volume number of Label  (3D Volume always equals 0, 4D Volume)

3) The attributes of the label that shall be measured

    1) Volume
    2) Center of Mass in index units - This helps with locating the lesion
    3) Dimensions of minimum bounding box
    4) Minimum dimension of bounding box
    5) Volume of bounding box
    6) Fill Factor of bounding box (Volume of label/Volume of lesion)

4) The user shall be able to limit the labels reported.   This would be similar to the ability of the sort function.

    1) Limiting the output to a continuous range of values (minimum and maximum)

5) The user shall be able to sort output of data by a single column.


Limitations

    1D label and image files shall not be supported.
    2D label and image files may be supported but they shall be treated as a 3D image with a single slice.

"""
from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
import numpy as np
from numpy import linalg
from random import random

import nibabel as nb
import pandas as pd
import scipy.ndimage as ndimage
import argparse

from scipy.ndimage.morphology import binary_erosion, binary_dilation, binary_opening

import iw_labels as labels
import scipy.stats as stats

def check_limits( parameter, limits ):
    return parameter >= limits[0] and parameter <= limits[1]


def calculate_bounding_box( mask ):

         objs    =  ndimage.find_objects(mask)

         bb_height = int(objs[0][0].stop - objs[0][0].start)
         bb_width  = int(objs[0][1].stop - objs[0][1].start)
         bb_depth  = int(objs[0][2].stop - objs[0][2].start)

         bb_min    = np.min( [ bb_height, bb_width, bb_depth ]) 
         bb_volume = bb_height * bb_width * bb_depth

         return [ bb_height, bb_width, bb_depth, bb_min, bb_volume ]

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='iw_compare_images')

     parser.add_argument("in_label_nii_filename",  help="Label NIFTI filename ")
     parser.add_argument("--out",                  help="Filename of CSV output file containing label stats", default=None)
     parser.add_argument("--stats",                help="Stats to report", type=str, nargs="*",
                         default=('volume', 'com_x', 'com_y', 'com_z', 'com_in', 'bb_dx', 'bb_dy', 'bb_dz', 'bb_dmin', 'bb_volume', 'fill_factor'  ))

     parser.add_argument("--labels",          help="Label indices to analyze", type=int, nargs="*", default = None )
     parser.add_argument("--sort",            help="Label indices to analyze", type=str, default = 'label' )

     parser.add_argument("--limits_volume",       help="Report labels within these limits", type=int, nargs=2, default = [0, np.inf] )
     parser.add_argument("--limits_fill_factor",  help="Report labels within these limits", type=int, nargs=2, default = [0, 1.0] )
     parser.add_argument("--limits_bb_volume",  help="Report labels within these limits", type=int, nargs=2, default = [0, np.inf] )

     parser.add_argument("--limits_background",   help="Report background label (i.e label=0)", action="store_true", default=False )

     parser.add_argument("-d","--display",   help="Display Results", action="store_true", default=False )
     parser.add_argument("-v","--verbose",   help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--verbose_nlines", help="Number of lines to display (default=10)",     default=10 )

     inArgs = parser.parse_args()

     label_nii    = labels.read_nifti_file( inArgs.in_label_nii_filename, 'Label file does not exist' )
     label_array  = label_nii.get_data()

     label_list = labels.get_labels( inArgs.labels, label_array, inArgs.limits_background)

     df_stats  = pd.DataFrame(columns= ('label', 'volume', 'com_x', 'com_y', 'com_z', 'com_in', 'bb_dx', 'bb_dy', 'bb_dz', 'bb_dmin', 'bb_volume', 'fill_factor' ) )

     stats_list = ['label',] + list(inArgs.stats)

     if inArgs.verbose:
         jj=0
         pd.set_option('expand_frame_repr', False)

     

     for ii in label_list:

         # Create logical mask
         mask = label_array == ii 

         # Calculate Volume
         label_volume = int(np.sum(  mask  ))
     
         if check_limits( label_volume,  inArgs.limits_volume ):

             bb_dx, bb_dy, bb_dz, bb_dmin, bb_volume = calculate_bounding_box( mask )
             
             if check_limits( bb_volume,  inArgs.limits_bb_volume ):

                 label_x_com, label_y_com, label_z_com = [ int(x) for x in np.round( ndimage.measurements.center_of_mass(mask), 0) ]
                 
                 label_com_in = mask[label_x_com, label_y_com, label_z_com]

                 fill_factor = label_volume / bb_volume
                 
                 if check_limits( fill_factor,  inArgs.limits_fill_factor ):
                     
                     label_stats = [ii, label_volume, label_x_com, label_y_com, label_z_com, label_com_in, bb_dx, bb_dy, bb_dz, bb_dmin, bb_volume, fill_factor ]
                     
                     df_stats.loc[len(df_stats)] = label_stats
                     
                     if inArgs.verbose:
                         if jj==(inArgs.verbose_nlines-1):
                             print
                             df_verbose =  df_stats.tail(inArgs.verbose_nlines) 
                             df_verbose = df_verbose[ stats_list ] 
                             print (df_verbose.to_string(formatters={'volume':'{:,.0f}'.format, 'x_com':'{:,.0f}'.format,'y_com':'{:,.0f}'.format,'z_com':'{:,.0f}'.format,
                                                                    'com_in':'{:,.0f}'.format, 'bb_dx':'{:,.0f}'.format, 
                                                                    'bb_dy':'{:,.0f}'.format,  'bb_dz':'{:,.0f}'.format,
                                                                    'bb_volume':'{:,.3f}'.format,  'fill_factor':'{:,.3}'.format}))
                             jj = 0
                         else:
                             jj += 1
                             

     df_sorted = df_stats.sort_values( [inArgs.sort], ascending=[1] ).reset_index(drop=True) 

     if inArgs.verbose:
         print
         print (df_sorted[ stats_list  ])
         print

     if not inArgs.out == None:
         df_sorted[ stats_list ].to_csv(inArgs.out, index=False ) 
