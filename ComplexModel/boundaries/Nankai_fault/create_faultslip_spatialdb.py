#!/usr/bin/env python

import numpy as np
from numpy import sin, cos, pi
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

deg2rad = pi/180.0

# Source model-related stuff
# xyzs = np.loadtxt("s1968HYUGAx01YAGI.fsp")
slips = np.loadtxt("s1946NANKAI01BABA.slp", comments="%")
# rakes = np.loadtxt("s2011TOHOKU01YAGI_slp.rake")

nx = 8
nz = 4
cellSizeX = 45.0 # km
cellSizeZ = 45.0 # km
faultDip = 12.0 # deg
faultStrike = 250.0 # deg
HypX = 85.0 # km
HypZ = 40.0 # km

# number of padding cells
nPadX = 2 # 2 on the left and 2 on the right
nPadZ = 2 # 2 on the bottom only.

# x and y offset to move the epicenter ((0,0) in .fsp file) to
# the model's epicenter coordinates.
xOffset = 1836.0
yOffset = 1453.64

# Open the spatialdb file
fdb = open("finalslip.spatialdb","w")
# print headers of spatialdb
header = '''// -*- C++ -*- (tell Emacs to use C++ mode for syntax highlighting)
#SPATIAL.ascii 1
SimpleDB {{
  num-values = 3
  value-names =  left-lateral-slip  reverse-slip  fault-opening
  value-units =  m  m  m
  num-locs = {0:d}
  data-dim = 2 // Locations of data points form a plane
  space-dim = 3
  cs-data = cartesian {{
    to-meters = 1.0e+3 // Specify coordinates in km for convenience.
    space-dim = 3
  }} // cs-data
}} // SimpleDB
// Columns are
// (1) x coordinate (km)
// (2) y coordinate (km)
// (3) z coordinate (km)
// (4) left-lateral-slip (m) (right-lateral is negative)
// (5) reverse-slip (m)
// (6) fault-opening (m)\
'''.format((nx+2*nPadX)*(nz+nPadZ))
print(header, file=fdb)

for j in range(nz+nPadZ):
    for i in range(nx+2*nPadX):
        # compute the center location of this cell
        # in the Cartesian coordinate system
        # (i.e., with the origin on the top left corner)
        #  < fault-local coordinate system >
        #    __________
        #    |         |
        #    |         |
        # x  |         |
        # ^  |  x  <- hypocenter (HypX, HypZ)
        # |  |         |
        # |  -----------
        # |-------- > z
        #
        # However, x, y coordinates below are north and east coordinates.
        # y ^
        #   |
        #   -----> x
        x = cellSizeZ * ( j * cos(faultDip*deg2rad) + 0.5 )
        y = cellSizeX * ( (i - nPadX) + 0.5 )
        #print(x, y)

        # If the current cell is outside of the source model
        # set slip and rake to be zero.
        slip = 0.0
        rake = 82.0 # uniform rake for the source model
        # if inside, retrieve slip and rake from the source model.
        if i >= nPadX and i < (nx+nPadX) and j < nz:
            slip = slips[j,i-nPadX]
            # rake = rakes[j,i-nPadX]
        # compute reverse and (left-lateral positive) strike slip
        reverse_slip = slip * sin(rake*deg2rad)
        strike_slip = slip * cos(rake*deg2rad)

        # shift the xy coordinates so that the epicenter becomes the origin.
        # The epicenter location in the fault plane coordinate system
        # comes with the source model.
        x = x - HypZ * cos(faultDip*deg2rad) - cellSizeX # shift to the west by one cell to safely contain all the fault elements.
        y = y - HypX

        # Rotate the coordinate by the fault strike
        # around the epicenter
        x_rot = x * cos( -faultStrike * deg2rad ) - y * sin( -faultStrike * deg2rad )
        y_rot = x * sin( -faultStrike * deg2rad ) + y * cos( -faultStrike * deg2rad )

        # Finally, translate the rotated cell center by the epicenter offsets
        x_rot = x_rot + xOffset
        y_rot = y_rot + yOffset
        print(x_rot, y_rot)

        # write the central location of the cell and
        # the slips to a spatialDB file
        print("{0:g} {1:g} 0.0 {2:g} {3:g} 0.0".format(x_rot, y_rot, strike_slip, reverse_slip), file=fdb)
        #eprint("{0:g} {1:g} 0.0 {2:g} {3:g} 0.0".format(x, y, reverse_slip, strike_slip))

fdb.close()
