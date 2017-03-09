#!/usr/bin/env python
from __future__ import print_function

import numpy as np
from numpy import sin, cos, pi
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

deg2rad = pi/180.0

xyzs = np.loadtxt("s2011TOHOKU01YAGI_fsp.xyz")
slips = np.loadtxt("s2011TOHOKU01YAGI_slp.slip")
rakes = np.loadtxt("s2011TOHOKU01YAGI_slp.rake")

nx = 25
ny = 10
cellSizeX = 20.0 # km
cellSizeY = 20.0 # km
faultDip = 12.0 # deg
faultStrike = 200.0 # deg

# Since the given locations in .fsp file is the x-y coordinates of
# the top center of the cells, we compute the location of the cell centers.
distanceToCellCenter = 0.5*cellSizeY*cos(faultDip*deg2rad)
cellCenter_xOffset = distanceToCellCenter * sin((faultStrike+90.0)*deg2rad)
cellCenter_yOffset = distanceToCellCenter * cos((faultStrike+90.0)*deg2rad)

# x and y offset to move the epicenter ((0,0) in .fsp file) to
# the model's epicenter coordinates.
xOffset = 2697.00
yOffset = 1987.84

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
'''.format(nx*ny)
print(header, file=fdb)

for j in range(ny):
    for i in range(nx):
        n = i + nx * j
        # retireve the location, slip and rake of the current cell.
        xyz = xyzs[n, 2:4]
        slip = slips[j,i]
        rake = rakes[j,i]
        # compute the cell center location
        x = xyz[0] + cellCenter_xOffset + xOffset
        y = xyz[1] + cellCenter_yOffset + yOffset
        # compute reverse and (left-lateral positive) strike slip
        reverse_slip = slip * sin(rake*deg2rad)
        strike_slip = slip * cos(rake*deg2rad)
        # write the central location of the cell and
        # the slips to a spatialDB file
        print("{0:g} {1:g} 0.0 {2:g} {3:g} 0.0".format(x, y, reverse_slip, strike_slip), file=fdb)
        #eprint("{0:g} {1:g} 0.0 {2:g} {3:g} 0.0".format(x, y, reverse_slip, strike_slip))

fdb.close()
