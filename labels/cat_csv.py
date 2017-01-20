#!/usr/bin/env python

"""

"""
import pandas
import argparse
import os

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='display_stats')

     parser.add_argument("in_csv",  help='CSV filename')
     inArgs = parser.parse_args()



     if os.path.isfile(inArgs.in_csv):
          df = pandas.read_csv(inArgs.in_csv)     

     #
     #
     #

     pandas.set_option('expand_frame_repr', False)
     pandas.set_option('display.max_rows',len(df))

     print(df)
